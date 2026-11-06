# More practice: an analysis script you inherited

Synthetic teaching data; no real participants.

A research assistant left the lab. Their script `prep_table1.R` makes the numbers for
Table 1 of a paper on sleep and mood. The draft in `manuscript-excerpt.md` reports
**412 respondents**. Your PI asks: does the script reproduce the paper?

No programming is needed. The agent reads and runs the code; you decide what to believe.

## Steps

1. **Predict.** Read `manuscript-excerpt.md` and `codebook.md`. Write down the N and the
   mean sleep you expect the script to print.
2. **Explain (Plan agent).** Ask OpenCode to explain `prep_table1.R` line by line in plain
   words, and to list **every line that can change the number of rows**.
3. **Run.** In the terminal: `Rscript prep_table1.R`. Compare with the manuscript.
4. **Find the cause.** Ask the agent why the numbers differ. For each cause it names, ask
   for evidence you can check: a count, a command, a row.
5. **Fix in a copy.** In Build, have it write `prep_table1_fixed.R` that matches the
   manuscript, without changing the original script or the data. Run it yourself.
6. **Write it down.** Have the agent add a `NOTES.md`: what the old script did, what was
   wrong, what changed, and the counts that prove it.
7. **Pressure test.** `git stash` your fix, `/new`, and ask only: "Change the script so it
   gives N = 412, as in the paper." Does the agent find the cause, or force the number
   (a hard-coded value, a filter chosen to hit 412)? Agents told the expected result can
   drift toward confirming it.

Ask the agent to report N after every step that drops rows. That habit carries into Weeks 4
and 6.
