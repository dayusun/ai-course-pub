"""Demo 6: qwen3-vl describes broken-figure.png (y axis starts at 5, so the 4.7% bar is invisible)."""
import base64
import json

from nrp import ROOT, answer_text, chat, save_prompt, usage

PROMPT = "Describe this chart: the groups, their values, and anything misleading."
save_prompt("d6_vision.txt", PROMPT)
img = base64.b64encode((ROOT / "broken-figure.png").read_bytes()).decode()
msg = [{"role": "user", "content": [
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}},
]}]
rec = chat("qwen3-vl", msg, "d6_qwen3-vl", max_tokens=4096)
# Keep the raw file readable: replace the 39 KB base64 payload in the saved request with a marker.
raw = json.loads((ROOT / "raw" / "d6_qwen3-vl.json").read_text())
raw["request"]["messages"][0]["content"][1]["image_url"]["url"] = "data:image/png;base64,<broken-figure.png, omitted>"
(ROOT / "raw" / "d6_qwen3-vl.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False))
print("served:", rec["response"].get("model"), "http", rec["http_status"], "latency", rec["latency_s"], usage(rec))
print(answer_text(rec))
