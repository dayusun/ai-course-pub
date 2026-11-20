# The walking trial: the running project of Week 4

Synthetic teaching data; no real participants.

- `data/participants.csv`: one row per participant (arm, age, sex, bmi, years with
  diabetes, metformin). `data/readings.csv`: 8 glucose readings per participant and clinic
  visit. `data/data-dictionary.csv`: units, allowed ranges, missing codes.
- `analysis-plan.md`: the question, the sample, the models and the output, fixed before the
  analysis. The agent follows it; you approve any change to it.
- `extras/`: `AGENTS.md`, `opencode.json` (permissions; lets the course model see images),
  and the `/record` slash command.

The slides have every step. This file is the same work in one place.

## Part 1: set up

    cd ~/week-04/glucose-trial
    cp extras/AGENTS.md extras/opencode.json . && mkdir -p .opencode/commands
    cp extras/commands/*.md .opencode/commands/
    chmod a-w data/* && git init && git add -A && git commit -m "start"
    opencode

## Part 2: profile

"Write scripts/profile.R. For every column of both files in data/, print the type, the
number missing (count each missing code the dictionary lists separately), the min and max,
and the levels of each category. Flag any value outside the dictionary's allowed range and
any subject that appears twice in participants.csv. Print summaries only, never rows. Run
it, save its output to output/profile.txt, and list what it flagged."

Decide what to do with each flag the dictionary does not answer.

## Part 3: clean

"P26 appears twice in participants.csv with identical rows: keep one. Write
scripts/clean.R that follows the dictionary and the plan: 999 becomes missing, mmol/L is
converted to mg/dL, the duplicate participant row is dropped. Join the two files with
left_join(..., relationship = "many-to-one"), so a subject listed twice stops the script.
Save output/visit_means.csv: one row per participant and visit, with arm, the fasting
mean and the post-meal mean. Print how many rows each step changes. Then run it."

Check: `wc -l output/visit_means.csv` gives 115 (114 rows and the header).

## Part 4: the planned analysis

1. Outside the folder, write `~/week-04/my-expectations.txt`: n analysed per arm, and a
   range for the primary estimate, before the agent shows you any result.
2. Tab to **Plan**: "Plan scripts/analysis.R for the primary and both secondary analyses in
   analysis-plan.md, starting from output/visit_means.csv (the mixed model also needs the
   readings). Before any code, state: the analysis sample and its n per arm; how missing
   values are handled; each model formula; and every key the script will write to
   output/results.json, with how it is computed. Do not write any file."
3. Answer its questions; Tab to **Build**: "Now write and run scripts/analysis.R as
   planned, and show me its output."
4. Compare its numbers with `my-expectations.txt`. Explain every difference before you
   accept the result.

A long analysis can run in the background, so the agent's session does not hang:

    mkdir -p logs && nohup Rscript scripts/analysis.R > logs/analysis.log 2>&1 &
    echo $! > logs/analysis.pid
    tail logs/analysis.log

## Part 5: figures

- Figure 1 with ggplot2 (`scripts/figure.R`) and with matplotlib (`scripts/figure1.py`):
  the prompts are on the slides "Drawing Figure 1" and "The same figure in matplotlib".
- Open `output/fig1.png` yourself: does each panel show only its own arm's two means?
- The participant flow diagram as hand-written SVG (`output/flow.svg`): the prompt is on
  "Drawing the flow diagram". Check every count against the data yourself.

## Parts 7-9

- Sample size: the prompt on "Planning the next trial"; check one n with statsmodels.
- Cluster job script: the prompt on "Drafting a job script"; read it line by line.
- Rerun from a clean start, then `/record`:

      mv output output-old
      Rscript scripts/clean.R && Rscript scripts/analysis.R && Rscript scripts/figure.R
      cmp output/results.json output-old/results.json && echo "same results"
