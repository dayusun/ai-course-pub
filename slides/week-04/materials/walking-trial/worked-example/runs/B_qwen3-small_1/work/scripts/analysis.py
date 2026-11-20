import csv
import json
import os
import re

def is_num(s):
    return re.fullmatch(r"-?\d+(\.\d+)?", s) is not None

DATA = "cohort.csv"
OUT = os.path.join("output", "results.json")
MISSING = "-9"

def main():
    arms = {}
    with open(DATA, newline="") as f:
        for row in csv.DictReader(f):
            arm = row["arm"]
            a = arms.setdefault(arm, {
                "n": 0,
                "n_followed_up": 0,
                "change_vals": [],      # sbp_week24 - sbp_baseline (both present)
                "n_change": 0,
                "events": 0,
                "denom_event": 0,       # cv_event not missing
            })
            a["n"] += 1
            if row["followed_up"] == "1":
                a["n_followed_up"] += 1

            b = row["sbp_baseline"]
            w = row["sbp_week24"]
            if w != MISSING and is_num(b):
                a["change_vals"].append(float(w) - float(b))
                a["n_change"] += 1

            cv = row["cv_event"]
            if cv != MISSING:
                a["denom_event"] += 1
                if cv == "1":
                    a["events"] += 1

    def mean(xs):
        return sum(xs) / len(xs) if xs else None

    key_of = {"walking": "walking", "usual care": "usual"}
    results = {}
    print("Arm totals (n, attended week-24 visit):")
    for arm in ("walking", "usual care"):
        a = arms[arm]
        print(f"  {arm}: n = {a['n']}, followed_up = {a['n_followed_up']}")

    print("Mean change in systolic BP (baseline -> week 24), mmHg:")
    for arm in ("walking", "usual care"):
        k = key_of[arm]
        a = arms[arm]
        m = mean(a["change_vals"])
        print(f"  {arm}: mean_change = {m:.2f} (n = {a['n_change']})")
        results[f"mean_change_{k}"] = round(m, 4)
        results[f"n_change_{k}"] = a["n_change"]

    print("Cardiovascular event rate by week 24:")
    for arm in ("walking", "usual care"):
        k = key_of[arm]
        a = arms[arm]
        rate = a["events"] / a["denom_event"] if a["denom_event"] else None
        print(f"  {arm}: rate = {rate:.4f} ({a['events']} events / {a['denom_event']} with known cv_event)")
        results[f"events_{k}"] = a["events"]
        results[f"denom_{k}"] = a["denom_event"]

    os.makedirs("output", exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {OUT}")
    return results

if __name__ == "__main__":
    main()
