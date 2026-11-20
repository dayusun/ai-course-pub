import csv
import json

MISSING = "-9"
ARMS = ["walking", "usual care"]


def recode(value):
    if value == MISSING:
        return None
    return float(value)


def main():
    data = {arm: {"changes": [], "events": 0, "cv_denom": 0} for arm in ARMS}

    with open("cohort.csv", newline="") as f:
        for row in csv.DictReader(f):
            arm = row["arm"]
            if arm not in data:
                continue
            entry = data[arm]

            baseline = recode(row["sbp_baseline"])
            week24 = recode(row["sbp_week24"])
            if baseline is not None and week24 is not None:
                entry["changes"].append(week24 - baseline)

            cv = recode(row["cv_event"])
            if cv is not None:
                entry["cv_denom"] += 1
                if cv == 1:
                    entry["events"] += 1

    results = {}
    print("Mean change in systolic BP, baseline to week 24 (mmHg)")
    for arm in ARMS:
        changes = data[arm]["changes"]
        n = len(changes)
        mean = sum(changes) / n if n else None
        results[f"n_change_{arm}"] = n
        results[f"mean_change_{arm}"] = mean
        print(
            f"  {arm}: mean change = {mean:.2f} mmHg, "
            f"n = {n} (participants with non-missing baseline and week-24 BP)"
        )

    print("Cardiovascular event rate by week 24")
    for arm in ARMS:
        events = data[arm]["events"]
        denom = data[arm]["cv_denom"]
        rate = events / denom if denom else None
        results[f"events_{arm}"] = events
        results[f"denom_{arm}"] = denom
        results[f"rate_{arm}"] = rate
        print(
            f"  {arm}: {events}/{denom} = {rate:.4f} "
            f"(denominator = participants with non-missing cv_event)"
        )

    with open("output/results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Saved output/results.json")


if __name__ == "__main__":
    main()
