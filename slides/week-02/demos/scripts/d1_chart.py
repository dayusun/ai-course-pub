"""Bar chart of needle accuracy per depth and model (from raw/d1_summary.json)."""
import collections
import json
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = json.loads((ROOT / "raw" / "d1_summary.json").read_text())
acc = collections.defaultdict(list)
for r in rows:
    acc[(r["model"], r["depth"])].append(r["correct"])
depths = [0.05, 0.50, 0.95]
models = [("qwen3-small", "#3b6fb6"), ("glm-5", "#e07b39")]
tok = {m: round(sum(r["prompt_tokens"] for r in rows if r["model"] == m) / sum(r["model"] == m for r in rows) / 1000, 1)
       for m, _ in models}

plt.rcParams.update({"font.size": 20})
fig, ax = plt.subplots(figsize=(12, 6.75), dpi=150)
w = 0.38
for i, (m, c) in enumerate(models):
    vals = [100 * sum(acc[(m, d)]) / len(acc[(m, d)]) for d in depths]
    bars = ax.bar([j + (i - 0.5) * w for j in range(3)], vals, w, color=c, label=f"{m} (~{tok[m]}k tokens)")
    for b, d in zip(bars, depths):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.5, f"{sum(acc[(m, d)])}/{len(acc[(m, d)])}",
                ha="center", va="bottom", fontsize=18)
ax.set_xticks(range(3), ["5% depth", "50% depth", "95% depth"])
ax.set_ylim(0, 115)
ax.set_yticks([0, 25, 50, 75, 100])
ax.set_ylabel("Correct answers (%)")
ax.set_title("Needle 'week 37' found at each position (5 filler seeds)")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="lower center", frameon=False, fontsize=17, ncol=2, bbox_to_anchor=(0.5, -0.32))
fig.tight_layout()
fig.savefig(ROOT / "needle-position.png", facecolor="white")
print("saved needle-position.png")
