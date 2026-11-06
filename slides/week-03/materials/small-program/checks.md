# Known answers (for you, not for the agent)

## Option A, on ../inherited-analysis/survey.csv

- 412 rows, 7 columns.
- `sleep_hours`: 6 values of -99 (the missing code), so the range starts at -99 unless they
  are flagged. Without them: 406 values.
- `income_band`: 44 cells with the text `NA` (how R writes a missing value), no empty cells.
- No other column has `NA`, empty cells or -99.

## Option B, from R

    power.t.test(delta = 0.5, sd = 1, sig.level = 0.05, power = 0.80)  # n = 63.8 -> 64
    power.t.test(delta = 0.8, sd = 1, sig.level = 0.05, power = 0.80)  # n = 25.5 -> 26
    power.t.test(delta = 0.2, sd = 1, sig.level = 0.05, power = 0.90)  # n = 526.3 -> 527

The normal approximation, 2 * (z(1 - alpha/2) + z(power))^2 / d^2, gives 63 for d = 0.5:
one fewer, because it ignores that the t distribution has heavier tails.
