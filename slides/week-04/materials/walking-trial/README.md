# The walking trial, October version (more practice)

A synthetic 300-patient trial (`cohort.csv`, `data-dictionary.csv`) and an analysis
request (`analysis-request.md`). `worked-example/` has the runs behind the backup slide
"October's worked example": the same request with a plain prompt and with `AGENTS.md`,
each run twice, and the verifier.

1. Copy `worked-example/AGENTS.md` into this folder; `chmod a-w *.csv`; `git init`.
2. Outside the folder, write down the sample size and a range for the change in systolic
   BP.
3. `opencode`, Plan first: check the denominator of the event rate before you Build.
   Over 150 randomized, or over those followed up? That choice is yours.
4. Run `worked-example/verifier/check_results.py` yourself, from outside the folder.
