"""Plot the week-24 event rate by arm (synthetic data). Contains errors to find."""
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open("figure-source.csv", newline="")))
arms = [r["arm"] for r in rows]
# event rate = events / randomised   (check the denominator)
rates = [100 * int(r["events"]) / int(r["randomised"]) for r in rows]

fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
ax.bar(["Usual care", "Walking"], rates, color=["#2a78d6", "#eb6834"])
ax.set_ylim(5, 12)
ax.set_ylabel("Cardiovascular events (%)")
ax.set_title("Events by week 24 (synthetic)")
for x, v in enumerate(rates):
    ax.text(x, v + 0.1, f"{v:.1f}%", ha="center")
fig.tight_layout()
fig.savefig("broken-figure.png")
