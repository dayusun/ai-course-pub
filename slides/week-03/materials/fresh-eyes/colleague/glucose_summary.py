"""Summaries of the tidy glucose table (the format the merge produces)."""
import csv

MMOL_TO_MGDL = 18.016


def read_rows(path):
    """One dict per reading: participant, visit, glucose (float, or None if missing), unit."""
    with open(path, newline="") as fh:
        return [
            {
                "participant": r["participant"],
                "visit": int(r["visit"]),
                "glucose": float(r["glucose"]) if r["glucose"] else None,
                "unit": r["unit"],
            }
            for r in csv.DictReader(fh)
        ]


def mean_per_participant(rows, low=20, high=600):
    """Mean glucose (mg/dL) per participant, implausible and missing readings excluded."""
    groups = {}
    for r in rows:
        groups.setdefault(r["participant"], []).append(r["glucose"])
    out = {}
    for p, vals in groups.items():
        kept = [v for v in vals if v is not None and low < v < high]
        out[p] = {"mean": round(sum(kept) / len(kept), 1), "n": len(vals)}
    return out


if __name__ == "__main__":
    for p, s in mean_per_participant(read_rows("data/readings.csv")).items():
        print(f"{p}  mean {s['mean']:6.1f} mg/dL  (n = {s['n']})")
