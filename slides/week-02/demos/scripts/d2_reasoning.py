"""Demo 2: reasoning effort on a pooled-SD + 95% CI question. 3 repeats per model x setting, temperature 0."""
import json
import re
from concurrent.futures import ThreadPoolExecutor

from nrp import ROOT, chat, save_prompt, usage

PROMPT = (
    "Two groups of adults had systolic blood pressure measured.\n"
    "Group A: n = 25, mean = 132.4 mmHg, SD = 10.2.\n"
    "Group B: n = 30, mean = 126.1 mmHg, SD = 11.8.\n"
    "Assuming equal variances, compute the pooled standard deviation and the 95% confidence interval "
    "for the difference in means (A minus B) using the t distribution. Give both to two decimals.\n"
    "End with exactly one line: ANSWER: pooled_sd=<x>; ci=(<lo>, <hi>)"
)
TRUTH = {"pooled_sd": 11.10, "lo": 0.27, "hi": 12.33}
SETTINGS = {
    "qwen3-small": {
        "off": {"chat_template_kwargs": {"enable_thinking": False}},
        "low": {"reasoning_effort": "low"},
        "high": {"reasoning_effort": "xhigh"},
    },
    "glm-5": {
        "off": {"chat_template_kwargs": {"enable_thinking": False}},
        "low": {"reasoning_effort": "low"},
        "high": {"reasoning_effort": "high"},
    },
}
save_prompt("d2_reasoning.txt", PROMPT)


def grade(text):
    m = re.search(r"ANSWER:\s*pooled_sd\s*=\s*([-\d.]+)\s*;\s*ci\s*=\s*\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)", text)
    if not m:
        return None, "no ANSWER line"
    sd, lo, hi = map(float, m.groups())
    ok = abs(sd - TRUTH["pooled_sd"]) <= 0.02 and abs(lo - TRUTH["lo"]) <= 0.02 and abs(hi - TRUTH["hi"]) <= 0.02
    return {"pooled_sd": sd, "lo": lo, "hi": hi}, "correct" if ok else "wrong"


def run(job):
    model, setting, rep = job
    rec = chat(model, [{"role": "user", "content": PROMPT}], f"d2_{model}_{setting}_r{rep}", max_tokens=16384,
               **SETTINGS[model][setting])
    text = ((rec["response"] or {}).get("choices") or [{}])[0].get("message", {}).get("content") or ""
    parsed, verdict = grade(text)
    return {"model": model, "setting": setting, "rep": rep, "http": rec["http_status"], "latency_s": rec["latency_s"],
            "parsed": parsed, "verdict": verdict, **usage(rec)}


jobs = [(m, s, r) for m in SETTINGS for s in SETTINGS[m] for r in (1, 2, 3)]
with ThreadPoolExecutor(max_workers=6) as ex:
    rows = list(ex.map(run, jobs))
(ROOT / "raw" / "d2_summary.json").write_text(json.dumps(rows, indent=1))
for r in rows:
    print(f"{r['model']:12} {r['setting']:5} r{r['rep']} {r['verdict']:8} {r['parsed']} lat={r['latency_s']}s "
          f"compl={r['completion_tokens']} reas={r['reasoning_tokens']}")
