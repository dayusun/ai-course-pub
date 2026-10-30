"""Demo 2 probe: which reasoning control does NRP honour? Same short question, different parameters."""
import json

from nrp import chat, usage

Q = [{"role": "user", "content": "What is 17 * 23? Answer with the number."}]
VARIANTS = {
    "default": {},
    "effort_low": {"reasoning_effort": "low"},
    "effort_high": {"reasoning_effort": "high"},
    "thinking_off": {"chat_template_kwargs": {"enable_thinking": False}},
    "thinking_on": {"chat_template_kwargs": {"enable_thinking": True}},
    "glm_thinking_disabled": {"thinking": {"type": "disabled"}},
}
rows = []
for model in ["qwen3-small", "glm-5"]:
    for name, params in VARIANTS.items():
        rec = chat(model, Q, f"d2_probe_{model}_{name}", max_tokens=4096, **params)
        msg = ((rec["response"] or {}).get("choices") or [{}])[0].get("message", {})
        reasoning = msg.get("reasoning_content") or msg.get("reasoning") or ""
        rows.append({
            "model": model, "variant": name, "http": rec["http_status"], "latency_s": rec["latency_s"],
            "answer": (msg.get("content") or "").strip()[:40], "reasoning_chars": len(reasoning), **usage(rec),
            "error": (rec["response"] or {}).get("error", {}).get("message", "")[:120] if isinstance((rec["response"] or {}).get("error"), dict) else (rec["response"] or {}).get("error"),
        })
print(json.dumps(rows, indent=1))
