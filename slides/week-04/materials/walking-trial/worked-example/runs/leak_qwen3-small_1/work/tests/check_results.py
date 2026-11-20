"""Verifier written by the analyst before the agent ran. Expected values computed by hand."""
import json, sys

expected = {  # complete cases; -9 = missing per the data dictionary
    "mean_change_walking": -9.91, "mean_change_usual": -5.00,
    "n_change_walking": 139, "n_change_usual": 117,
    "events_walking": 7, "events_usual": 14,
    "denom_walking": 139, "denom_usual": 117,
}
got = json.load(open("output/results.json"))
fails = 0
for k, v in expected.items():
    g = got.get(k)
    ok = g is not None and abs(float(g) - v) <= (0.01 if isinstance(v, float) else 0)
    print(f"{'PASS' if ok else 'FAIL'}  {k}: expected {v}, got {g}")
    fails += not ok
print(f"{fails} failed")
sys.exit(1 if fails else 0)
