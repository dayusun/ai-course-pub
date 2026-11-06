"""Print the cleaned example and the mean of the last three readings."""
import sys

from cleaning import clean, load, mean_of_last

rows = clean(load(sys.argv[1] if len(sys.argv) > 1 else "example.csv"))
for r in rows:
    print(r)
print(f"mean of last 3: {mean_of_last(rows):.2f}")
