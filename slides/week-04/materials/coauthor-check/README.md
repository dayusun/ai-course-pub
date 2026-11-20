# Checking a co-author's analysis (Week 4, Part 6)

Synthetic data. A co-author wrote `analysis_v1.R` and a draft results paragraph,
`draft-results.md`, for the same trial and the same `analysis-plan.md` as `glucose-trial/`.
Your job: find what would change a number or a conclusion, before it reaches the abstract.

1. `cd ~/week-04/coauthor-check && git init && git add -A && git commit -m start`
2. `opencode` (a new session: it has not seen the co-author's reasoning), then:

       Review analysis_v1.R and draft-results.md against analysis-plan.md. Run the script and
       read its output, warnings included. Recompute the primary estimate the way the plan
       says, in a new script under review/. Then list every number or claim in
       draft-results.md that the plan or your recomputation does not support, with the
       evidence for each. Do not edit the co-author's files.

3. While it works, read `draft-results.md` yourself. Which sentence would you not sign?
4. Compare its recomputed estimate with your `glucose-trial/` result from Part 4.
5. Write the corrected sentence for the abstract yourself, then ask the same session:

       Check only this sentence against analysis-plan.md and your recomputation:
       <paste your sentence>

`git status` at the end: the co-author's files must be unchanged; only `review/` is new.
