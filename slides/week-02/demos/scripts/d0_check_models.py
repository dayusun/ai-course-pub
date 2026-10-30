"""Demo 0: which underlying model each alias serves (one short request each)."""
import json
from datetime import datetime, timezone

from nrp import ROOT, chat, post

out = {"utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "aliases": {}}
for alias in ["qwen3-small", "glm-5", "qwen3-vl"]:
    rec = chat(alias, [{"role": "user", "content": "Reply with OK."}], f"d0_check_{alias}", max_tokens=16)
    out["aliases"][alias] = {"served": (rec["response"] or {}).get("model"), "http": rec["http_status"], "latency_s": rec["latency_s"]}
rec = post("/embeddings", {"model": "qwen3-embedding", "input": ["ping"]}, "d0_check_qwen3-embedding")
emb = rec["response"] or {}
out["aliases"]["qwen3-embedding"] = {
    "served": emb.get("model"),
    "http": rec["http_status"],
    "dim": len(emb["data"][0]["embedding"]) if emb.get("data") else None,
}
(ROOT / "raw" / "d0_summary.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
