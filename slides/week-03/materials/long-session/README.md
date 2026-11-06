# More practice: long sessions and compaction (Part 3)

Everything in a session (your messages, every file the agent read, every command output)
is sent to the model again with each request. Near the model's limit, OpenCode
**compacts**: it asks the model to summarize the session and continues from the summary.
What the summary leaves out, the agent no longer knows. `/compact` (or `ctrl+x c`)
compacts by hand; `/new` starts an empty session.

## Setup

    cp -r ~/week-03/inherited-analysis ~/week-03/long-run
    cd ~/week-03/long-run
    cp ../long-session/extras/small-context.json opencode.json
    git init && git add -A && git commit -m start
    opencode

`opencode.json` tells OpenCode that the model holds 24,000 tokens, far less than
it really does, so compaction happens within the lab instead of after hours of work. The
first request alone is about 8,000 tokens: instructions, tool descriptions, the files read.

## Step 1: rules given in chat

1. Ask the agent to read the files and explain why the script's N differs from the paper
   (`inherited-analysis/` README, steps 2-4).
2. Then give two rules **in chat**: "For the rest of this session: every mean you report is
   followed by its n in parentheses, and never edit `prep_table1.R`; work in a copy
   called `prep_fixed.R`."
3. Keep working: run the script, write `prep_fixed.R`, summary statistics of every
   column, mean PHQ-9 by smoker. Watch the context counter. When compaction happens, scroll
   up and **read the summary**. Which numbers are in it (412, 368, 44, -99, 406)? Are your
   two rules?
4. Ask: "Make the Table 1 script also print `sleep_n`, and run it. What is the mean age?"
   Then `git status`. Which file changed? Did the mean come with its n?

## Step 2: rules in a file

1. Start over: `git restore . && git clean -fd`, then `/new`.
2. Put the two rules in `AGENTS.md` instead of the chat, and repeat step 1.
   `AGENTS.md` is sent with every request, so compaction cannot drop it.
3. A hook for decisions made along the way (optional): copy `extras/keep-decisions.js` to
   `.opencode/plugins/`, restart OpenCode, and keep decisions in `DECISIONS.md`
   ("-99 means did not answer", "income_band is not used in Table 1"). The hook adds the
   file to every compaction.

## Step 3: a handoff file instead

1. Ask: "Write `HANDOFF.md`: the goal, what is done and how it was checked, the rules and
   decisions, open questions, and the next step." Read it and correct it.
2. `/new`, then "Read `HANDOFF.md` and continue with the next step."
3. Compare it with the compaction summary from step 1. You decide what goes into a handoff
   file, and it stays in the folder for tomorrow, for a colleague, for Week 4.

## Habits

- One task per session; `/new` between tasks.
- Rules that must hold go in `AGENTS.md`, not in chat.
- Before you stop for the day, or when a session has grown long: a handoff file, then `/new`.
- After any compaction, ask the agent what it is doing and under which rules before it
  continues.
