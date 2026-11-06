# Part 8: a goal and a loop

A long session keeps going and compacts (Part 3). Here every step gets a **fresh session**:
the same prompt runs again and again, and what the agent knows between runs is only what is
in the files (`PLAN.md`, `NOTES.md`, `git log`). This is the *Ralph loop*. What decides that
the work is finished is a **goal check**, `check.sh`, a command: every test passes and the
tests are unchanged. The agent saying "done" does not count.

The work: four small functions for the glucose study's exports (the merge of Part 4). The tests are already
written (`tests/`); they are the spec, and the agent may not change them.

## Setup

    cp -r ~/week-03/goal-loop ~/week-03/goal-run
    cd ~/week-03/goal-run
    git init && git add -A && git commit -m start && git tag start
    sh check.sh

`check.sh` fails: nothing is implemented yet. Read `PROMPT.md`, `PLAN.md`, `check.sh` and
`opencode.json` before you start the loop. `opencode.json` denies edits in `tests/` and a
few git commands, because the loop runs with `--auto` (Part 4): no one approves each step.

## Step 1: run the loop

    sh ralph.sh 6

Each pass is one `opencode run` with no memory of the last. Watch it, or leave it and come
back. When it stops:

- `git log --oneline`: one commit per item? In order?
- `NOTES.md`: what did each pass leave for the next?
- `sh check.sh` yourself, and `git diff start -- tests` (should be empty).
- How many passes did it take? Did any pass do more than one item, or none?

## Step 2: compare with a long session

In the Part 3 test, a long session lost rules when it was compacted again and again. Here no session lives long
enough to be compacted. What carries over, and who decides what goes into it? What would
you lose if `NOTES.md` were badly written?

## Step 3: what counts as done

1. Open `check.sh`. What could an agent do to make it pass without doing the work? (Which
   of those does `opencode.json` block, and which does the check itself catch?)
2. A weaker goal: change the first line of `PROMPT.md` to also say "When every item is
   ticked, write ALL DONE in NOTES.md", and imagine the loop stopping on
   `grep -q "ALL DONE" NOTES.md` instead. Why is that worse?
3. To rerun: `git reset --hard start && git clean -fdx` (you can, the agent cannot).

## The same idea in other agents

- **Claude Code** `/goal <condition>` and **Codex** `/goal`: after each turn, a model checks
  the condition and, if it is not met, the agent takes another turn. Claude Code's checker
  reads only the conversation and runs nothing itself, so write the condition as something
  a command shows: "`python3 -m pytest -q tests` passes and `git diff start -- tests` is
  empty, or stop after 10 turns".
- These loops keep one session (and compact it); `ralph.sh` starts a new one each pass.
- In every version: a check that is a command, a limit on passes or turns, deny rules, and
  a commit per step so you can see and undo each one.
