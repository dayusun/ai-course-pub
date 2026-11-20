import csv

MISSING = "-9"
EXPECTED_COLS = [
    "id",
    "arm",
    "age",
    "sbp_baseline",
    "sbp_week24",
    "followed_up",
    "cv_event",
]


def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def main():
    problems = {col: 0 for col in EXPECTED_COLS}
    rows = 0
    valid_ids = {f"S{i:03d}" for i in range(1, 301)}
    valid_arms = {"walking", "usual care"}
    valid_age = {str(i) for i in range(40, 80)} | {MISSING}
    valid_followed_up = {"0", "1"}
    valid_cv_event = {"0", "1", MISSING}

    with open("cohort.csv", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != EXPECTED_COLS:
            print("COLUMNS_MISMATCH", reader.fieldnames)
        for row in reader:
            rows += 1
            if row["id"] not in valid_ids:
                problems["id"] += 1
            if row["arm"] not in valid_arms:
                problems["arm"] += 1
            if row["age"] not in valid_age:
                problems["age"] += 1
            # dictionary lists no missing code for sbp_baseline
            if not is_numeric(row["sbp_baseline"]) or row["sbp_baseline"] == MISSING:
                problems["sbp_baseline"] += 1
            if not is_numeric(row["sbp_week24"]):
                problems["sbp_week24"] += 1
            if row["followed_up"] not in valid_followed_up:
                problems["followed_up"] += 1
            if row["cv_event"] not in valid_cv_event:
                problems["cv_event"] += 1

    print(f"rows: {rows}")
    total = 0
    for col in EXPECTED_COLS:
        n = problems[col]
        total += n
        print(f"{col}: {n} problems")
    print(f"total problems: {total}")


if __name__ == "__main__":
    main()
