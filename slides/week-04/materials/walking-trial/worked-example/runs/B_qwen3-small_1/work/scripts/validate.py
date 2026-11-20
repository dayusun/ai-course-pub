import csv
import re
import sys
from collections import Counter

DATA = "cohort.csv"

EXPECTED_IDS = {f"S{i:03d}" for i in range(1, 301)}
ARM_VALUES = {"walking", "usual care"}
AGE_MIN, AGE_MAX = 40, 79
MISSING = "-9"
SBP_MIN, SBP_MAX = 60, 250
COLUMNS = ["id", "arm", "age", "sbp_baseline", "sbp_week24", "followed_up", "cv_event"]

def is_int(s):
    return re.fullmatch(r"-?\d+", s) is not None

def is_num(s):
    return re.fullmatch(r"-?\d+(\.\d+)?", s) is not None

def main():
    problems = {c: 0 for c in COLUMNS}
    id_counts = Counter()
    n_rows = 0

    with open(DATA, newline="") as f:
        for row in csv.DictReader(f):
            n_rows += 1

            # id: S001-S300, unique
            id_counts[row["id"]] += 1

            # arm: walking; usual care
            if row["arm"] not in ARM_VALUES:
                problems["arm"] += 1

            # age: integer 40-79, -9 = missing
            a = row["age"]
            if not is_int(a):
                problems["age"] += 1
            elif a != MISSING and not (AGE_MIN <= int(a) <= AGE_MAX):
                problems["age"] += 1

            # sbp_baseline: numeric
            b = row["sbp_baseline"]
            if not is_num(b) or not (SBP_MIN <= float(b) <= SBP_MAX):
                problems["sbp_baseline"] += 1

            # sbp_week24: numeric, -9 = missing
            w = row["sbp_week24"]
            if w != MISSING and (not is_num(w) or not (SBP_MIN <= float(w) <= SBP_MAX)):
                problems["sbp_week24"] += 1

            # followed_up: 1 or 0
            if row["followed_up"] not in {"0", "1"}:
                problems["followed_up"] += 1

            # cv_event: 1, 0, or -9 missing
            if row["cv_event"] not in {"0", "1", MISSING}:
                problems["cv_event"] += 1

    problems["id"] = sum(n for i, n in id_counts.items() if i not in EXPECTED_IDS) + \
                     sum(n - 1 for n in id_counts.values() if n > 1)

    print(f"Rows checked: {n_rows}")
    print(f"Expected ids: {len(EXPECTED_IDS)}, distinct ids found: {len(id_counts)}")
    print("Problems per column:")
    for col in COLUMNS:
        print(f"  {col}: {problems[col]}")
    total = sum(problems.values())
    print(f"Total problems: {total}")
    return 0 if total == 0 and n_rows == 300 else 1

if __name__ == "__main__":
    sys.exit(main())
