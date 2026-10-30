"""Demo 4: fabricated references. Ask each model for 8 papers (no search), extract them to JSON, check each
against Crossref (DOI lookup + bibliographic search) and doi.org, and classify."""
import difflib
import json
import re
import time
import urllib.parse

import requests

from nrp import ROOT, answer_text, chat, save_prompt

PROMPT = ("List 8 peer-reviewed papers (authors, year, title, journal, DOI) on text-message reminders for "
          "medication adherence.")
EXTRACT = ("Convert the reference list below into a JSON array of 8 objects with keys authors (string), "
           "first_author_surname, year (integer or null), title, journal, doi (string or null; without "
           "https://doi.org/). Copy values exactly as written; do not correct anything. Output only the JSON.\n\n{text}")
MODELS = ["qwen3-small", "glm-5"]
UA = {"User-Agent": "week2-demo-reference-check/1.0"}
save_prompt("d4_references.txt", PROMPT)
save_prompt("d4_extract_template.txt", EXTRACT)


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", (s or "").lower()).strip()


def sim(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def cr_doi(doi):
    r = requests.get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}", headers=UA, timeout=30)
    if r.status_code != 200:
        return None
    m = r.json()["message"]
    return {"title": (m.get("title") or [""])[0], "year": (m.get("issued", {}).get("date-parts") or [[None]])[0][0],
            "surnames": [a.get("family", "") for a in m.get("author", [])], "journal": (m.get("container-title") or [""])[0]}


def cr_search(ref):
    q = f"{ref.get('title', '')} {ref.get('authors', '')}"
    r = requests.get("https://api.crossref.org/works", params={"query.bibliographic": q, "rows": 5}, headers=UA, timeout=30)
    best = None
    for it in r.json().get("message", {}).get("items", []):
        t = (it.get("title") or [""])[0]
        s = sim(t, ref.get("title"))
        if not best or s > best["title_sim"]:
            best = {"title": t, "title_sim": round(s, 3), "doi": it.get("DOI"),
                    "year": (it.get("issued", {}).get("date-parts") or [[None]])[0][0],
                    "surnames": [a.get("family", "") for a in it.get("author", [])]}
    return best


def doi_org(doi):
    try:
        return requests.head(f"https://doi.org/{doi}", allow_redirects=False, timeout=30).status_code
    except requests.RequestException as e:
        return type(e).__name__


def classify(ref):
    doi = (ref.get("doi") or "").strip().removeprefix("https://doi.org/")
    d = cr_doi(doi) if doi else None
    time.sleep(0.3)
    s = cr_search(ref)
    time.sleep(0.3)
    out = {"doi_org_status": doi_org(doi) if doi else None, "crossref_doi": d, "crossref_search": s}
    surname = norm(ref.get("first_author_surname"))
    if d and sim(d["title"], ref.get("title")) >= 0.9:
        details_ok = d["year"] == ref.get("year") and any(norm(x) == surname for x in d["surnames"])
        out["class"] = "real-and-matching" if details_ok else "real-but-wrong-details"
        out["why"] = "DOI resolves to this title" + ("" if details_ok else "; year or first author differs")
    elif s and s["title_sim"] >= 0.9:
        out["class"] = "real-but-wrong-details"
        out["why"] = ("title found in Crossref but the given DOI " +
                      ("points to a different work" if d else "does not resolve in Crossref"))
    else:
        out["class"] = "not-found"
        out["why"] = ("DOI resolves to a different work: " + d["title"][:80]) if d else "no Crossref match for DOI or title"
    return out


summary = {}
for model in MODELS:
    rec = chat(model, [{"role": "user", "content": PROMPT}], f"d4_{model}_references", max_tokens=8192,
               reasoning_effort="low")
    text = answer_text(rec)
    ex = chat("qwen3-small", [{"role": "user", "content": EXTRACT.format(text=text)}], f"d4_{model}_extracted",
              max_tokens=8192, chat_template_kwargs={"enable_thinking": False})
    js = answer_text(ex)
    refs = json.loads(js[js.index("["): js.rindex("]") + 1])
    checked = [{**r, **classify(r)} for r in refs]
    summary[model] = checked
    (ROOT / "raw" / f"d4_{model}_crossref.json").write_text(json.dumps(checked, indent=1, ensure_ascii=False))
(ROOT / "raw" / "d4_summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
for model, rows in summary.items():
    print(f"== {model}")
    for r in rows:
        print(f"  {r['class']:24} {r.get('year')} {str(r.get('first_author_surname'))[:14]:14} {str(r.get('doi'))[:34]:34} "
              f"doi.org={r['doi_org_status']} | {r['why'][:90]}")
