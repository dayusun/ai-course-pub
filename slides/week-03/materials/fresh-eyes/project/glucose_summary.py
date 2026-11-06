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
