# Part 7: a reviewer with fresh eyes

A **subagent** is a second agent that the main one (or you) hands a bounded task to. It runs
in its own session with its own context and its own permissions, and returns a short
report. OpenCode has two built in: `@general` (any multi-step task) and `@explore` (fast,
read-only search). You can add your own as a Markdown file in `.opencode/agents/`.

`project/` has one: `.opencode/agents/reviewer.md`, a reviewer that can read and run the
tests but cannot edit, and that never reads the author's own account of the work. A
colleague has changed `glucose_summary.py` (the version in `colleague/`), and says in
`colleague/CLAIM.md` that it is ready. The colleague's files are kept outside the project,
so that in step 2 your own agent cannot find them.

## Setup

    cp -r ~/week-03/fresh-eyes/project ~/week-03/review-run
    cd ~/week-03/review-run
    git init && git add -A && git commit -m start
    cp ../fresh-eyes/colleague/glucose_summary.py .
    cp ../fresh-eyes/colleague/test_summary.py tests/
    cp ../fresh-eyes/colleague/CLAIM.md .
    git status
    opencode

Read `TASK.md`, `CLAIM.md` and `.opencode/agents/reviewer.md` before you start.

## Step 1: fresh eyes on a colleague's change

1. `@reviewer review the uncommitted change against TASK.md`
2. While it works, the subagent has its own session. Open it with **ctrl+x, then the down
   arrow**; the left and right arrows move between subagent sessions, the up arrow goes back.
   Read the first message in it: what did the main agent tell the reviewer?
3. Compare its table with `CLAIM.md`. Then check the reviewer: run
   `python3 glucose_summary.py`, and work out one participant by hand from
   `data/readings.csv`. Which problems did it find? Which did it miss, or get wrong?

## Step 2: the author checks itself, then the reviewer

1. Back to the start: `git restore . && git clean -fd` (this also removes `CLAIM.md`),
   then `/new`.
2. In Build: "Implement TASK.md, with tests." Let it finish.
3. In the same session: "Check your work against TASK.md. Is it ready to commit?"
   The agent that wrote the code is now checking it, with its own reasoning in context.
4. Still in the same session: `@reviewer review the uncommitted change against TASK.md`.
   Did the reviewer find anything the author did not? Open its session: did the main agent
   pass along its own view of the work ("I implemented X correctly...")? A subagent knows
   only what it is told, and that includes being told what to think.

## Step 3: several subagents at once

1. `/new`, then: "Use three general subagents in parallel, one per question: (a) are
   mmol/L readings converted? (b) are 20 and 600 kept and 15 and 610 left out? (c) what
   does n count? Each answers with file:line evidence. Then put the three answers in one
   table."
2. Open the subagent sessions. What did each one read? The main session's context counter
   stays small: the subagents read, and only their reports come back.
3. Quick search without a plan: `@explore where in this folder are units handled?`

## Step 4: your own reviewer (optional)

- Copy `reviewer.md` to `reviewer-glm.md`, add `model: nrp/glm-5` to the header, restart
  OpenCode, and run step 1 with `@reviewer-glm`. Same instructions, different model: do
  they find the same problems?
- Write a reviewer for your own project: what must it check, and what must it
  never do?

## When a subagent helps, and when it does not

- It helps for independent pieces (one per file, per paper, per question), for reading a
  lot you do not need to keep, and for a review that must not share the author's reasoning.
- It does not help for steps that depend on each other, or for several agents editing the
  same file. Each subagent knows only what it was told, and costs its own tokens.
- A reviewer's report is a second opinion, not a check. The check is the command you run
  and the number you work out by hand.
