# WALK-G pilot analysis (synthetic data)

## Rules
- `data/` is read-only. Never edit, rename or overwrite anything in it.
- Read `data/data-dictionary.csv` and `analysis-plan.md` before writing any code.
- Never print data rows. Scripts print summaries only: counts, means, model estimates.
- Follow `analysis-plan.md`. No other models, subgroups or covariates unless I ask.
- Scripts go in `scripts/` (R), outputs in `output/`.
- Report the n behind every number, and say how many rows each step drops.
- If the plan or the dictionary does not cover a case, stop and ask.

## Done means
- The script runs from a clean start: `Rscript scripts/analysis.R`.
- `output/results.json` has every key the plan lists.
- You show me the commands you ran and their output, not a summary of them.
