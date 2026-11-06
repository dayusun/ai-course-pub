# Task given to the colleague

Add `mean_per_participant(rows, low=20, high=600)` to `glucose_summary.py`.

1. One result per participant, over all visits: `{"mean": ..., "n": ...}`.
2. Readings in mmol/L are converted to mg/dL first (x 18.016).
3. After conversion, readings below `low` or above `high` are implausible and left out.
   `low` and `high` themselves are plausible: 20 and 600 are kept.
4. Missing readings are left out.
5. `n` is the number of readings the mean was computed from.
6. A participant with no usable readings gets `{"mean": None, "n": 0}`.
7. The mean is rounded to one decimal.
8. Tests for the new function in `tests/test_summary.py`.
