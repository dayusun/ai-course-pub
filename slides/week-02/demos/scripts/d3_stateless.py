"""Demo 3: the API is stateless. Call 2 without and then with the history resent."""
import json

from nrp import ROOT, answer_text, chat, save_prompt

C1 = "My name is Dana and my study has 412 participants."
C2 = "How many participants are in my study?"
save_prompt("d3_call1.txt", C1)
save_prompt("d3_call2.txt", C2)
rows = []
for model in ["qwen3-small", "glm-5"]:
    p = {"reasoning_effort": "low"}
    r1 = chat(model, [{"role": "user", "content": C1}], f"d3_{model}_call1", max_tokens=2048, **p)
    a1 = answer_text(r1)
    r2 = chat(model, [{"role": "user", "content": C2}], f"d3_{model}_call2_no_history", max_tokens=2048, **p)
    hist = [{"role": "user", "content": C1}, {"role": "assistant", "content": a1}, {"role": "user", "content": C2}]
    r3 = chat(model, hist, f"d3_{model}_call2_with_history", max_tokens=2048, **p)
    rows.append({"model": model, "call1": a1, "call2_no_history": answer_text(r2), "call2_with_history": answer_text(r3)})
(ROOT / "raw" / "d3_summary.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
for r in rows:
    print(f"== {r['model']}")
    for k in ("call1", "call2_no_history", "call2_with_history"):
        print(f"  {k}: {r[k].strip()[:300]!r}")
