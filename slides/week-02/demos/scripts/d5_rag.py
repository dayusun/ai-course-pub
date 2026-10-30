"""Demo 5: tiny RAG over the three synthetic papers. One chunk per "p. N." paragraph, embedded with
qwen3-embedding, cosine top-k = 1 and 3, answered by qwen3-small from the retrieved chunks only."""
import json
import math
import re

from nrp import ROOT, answer_text, chat, post, save_prompt

QUESTION = "Did any trial measure ambulatory blood pressure?"
FILES = ["paper-walk1.md", "paper-walk2.md", "paper-stephtn.md"]


def chunks():
    out = []
    for f in FILES:
        text = (ROOT / f).read_text()
        title = text.splitlines()[0].lstrip("# ").strip()
        for m in re.finditer(r"\*\*(p\. \d+)\.\*\*\s*(.+?)(?=\n\n\*\*p\.|\Z)", text, re.S):
            out.append({"id": f"{f.split('-')[1].split('.')[0]}:{m.group(1)}", "paper": title,
                        "text": " ".join(m.group(2).split())})
    return out


def cos(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def keyword_score(q, t):
    qs = set(re.findall(r"[a-z]+", q.lower())) - {"did", "any", "trial", "measure"}
    return len(qs & set(re.findall(r"[a-z]+", t.lower())))


CH = chunks()
emb = post("/embeddings", {"model": "qwen3-embedding", "input": [QUESTION] + [c["text"] for c in CH]}, "d5_embeddings")
vecs = [d["embedding"] for d in sorted(emb["response"]["data"], key=lambda d: d["index"])]
qv, cv = vecs[0], vecs[1:]
ranked = sorted(({"rank": 0, **c, "cosine": round(cos(qv, v), 4), "keyword_overlap": keyword_score(QUESTION, c["text"])}
                 for c, v in zip(CH, cv)), key=lambda r: -r["cosine"])
for i, r in enumerate(ranked, 1):
    r["rank"] = i

TEMPLATE = ("Answer the question using only the excerpts below. If the excerpts do not contain the answer, say so.\n\n"
            "{ctx}\n\nQuestion: {q}")
save_prompt("d5_question.txt", QUESTION)
save_prompt("d5_template.txt", TEMPLATE)
# Keyword retriever: term overlap with the question, ties broken by document order.
kw_ranked = sorted(ranked, key=lambda r: (-r["keyword_overlap"], CH.index(next(c for c in CH if c["id"] == r["id"]))))
results = {"ranking": ranked, "runs": []}
for name, order in (("embedding", ranked), ("keyword", kw_ranked)):
    for k in (1, 3):
        ctx = "\n\n".join(f"[{r['id']}] {r['text']}" for r in order[:k])
        rec = chat("qwen3-small", [{"role": "user", "content": TEMPLATE.format(ctx=ctx, q=QUESTION)}],
                   f"d5_answer_{name}_top{k}", max_tokens=2048, reasoning_effort="low")
        results["runs"].append({"retriever": name, "k": k, "retrieved": [r["id"] for r in order[:k]],
                                "answer": answer_text(rec).strip()})
(ROOT / "raw" / "d5_summary.json").write_text(json.dumps(results, indent=1, ensure_ascii=False))
for r in ranked:
    print(f"{r['rank']:2} {r['id']:14} cos={r['cosine']:.4f} kw={r['keyword_overlap']} {r['text'][:80]}")
for run in results["runs"]:
    print(f"\n== {run['retriever']} top-{run['k']} retrieved {run['retrieved']}\n{run['answer'][:500]}")
