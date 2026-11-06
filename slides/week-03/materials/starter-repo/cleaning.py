"""Clean home blood-pressure readings (synthetic teaching example)."""
import csv

PLAUSIBLE = (70, 250)  # mmHg, inclusive


def load(path):
    """Read a CSV with columns id, day, sbp."""
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def clean(rows):
    """Keep readings with a plausible systolic value, as integers."""
    out = []
    for r in rows:
        sbp = int(r["sbp"])
        if PLAUSIBLE[0] <= sbp <= PLAUSIBLE[1]:
            out.append({"id": r["id"], "day": int(r["day"]), "sbp": sbp})
    return out


def mean_of_last(readings, k=3):
    """Mean systolic pressure of the last k readings, in day order."""
    readings = sorted(readings, key=lambda r: r["day"])
    last = readings[-k - 1:-1]
    return sum(r["sbp"] for r in last) / len(last)
