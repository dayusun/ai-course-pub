# Analysis project: walking trial (synthetic data)

## Rules
- Read `data-dictionary.csv` before writing any code. Recode every missing-value code it lists.
- Never print data rows. Scripts print summaries only (counts, means, rates).
- Do not edit `cohort.csv` or `data-dictionary.csv`.
- Put scripts in `scripts/`, outputs in `output/`.

## Workflow
1. Write `scripts/validate.py`: check every column against the dictionary (allowed values,
   ranges, missing codes) and print a count of problems per column. Run it.
2. Write `scripts/analysis.py`. For every number, report the n it is based on and the
   denominator of every rate.
3. Save results to `output/results.json` with keys:
   mean_change_walking, mean_change_usual, n_change_walking, n_change_usual,
   events_walking, events_usual, denom_walking, denom_usual.
4. Run both scripts from a clean start and report their output verbatim.
