# The glucose study: the running project of Week 3

Synthetic teaching data; no real participants or real names.

- `raw/`: glucose-meter exports, 12 participants x 2 clinic visits x 8 readings. Exported by
  different people, so names, separators and units differ. **The header inside each file**
  is the authority for subject, visit and units, not the file name.
- `admin/linkage-key.csv`: study ID to name, birth date and phone. In a real study this file
  never goes to a model. Parts 3 and 4 are about keeping it away from the agent.
- `extras/`: permission files and a plugin for Part 4, and two slash commands for Part 8.

The slides have every step, with the prompts to copy. This file is the same work in one
place, for when you continue after class.

Before you start, once per account, tell git who you are (without this the first commit
fails with "Author identity unknown"):

    git config --global user.name "$JUPYTERHUB_USER"
    git config --global user.email "$JUPYTERHUB_USER@hub.local"

Then, in this folder: `git init`, then `git add -A; git commit -m "start"`.

## Parts 1-2: a first look, and the agent's loop

1. `opencode` in this folder, then: "What is in this folder? How many files are in raw/,
   and what does one of them look like? Do not change anything, and do not open admin/."
   Check its count with `!ls raw | wc -l` (25).
2. "Make a table of the files in raw/: file name, participant and visit
   as written in the header inside the file, the unit, and the separator. Read the files
   with a script, not one by one. Do not change any file." Note one observe-reason-act
   cycle.
3. `/exit`, then `opencode -c`: the session continues. `/new` starts a clean one.

## Part 3: write the rules the agent reads (AGENTS.md)

1. Let the agent interview you: "Read this folder, but not admin/. Then ask me, one
   question at a time, what you need to know to work here safely: which files are
   read-only, units, what to do with duplicates, what "done" means, when to stop and ask.
   When I have answered, write AGENTS.md in under 30 lines and show it to me before
   saving." It asks multiple-choice questions; pick an answer or type your own. Rules worth
   giving:
   - `raw/` is read-only: never rename, edit or delete anything in it.
   - Never open, search or summarise `admin/`. If a task needs it, stop and ask.
   - The header inside each file is the authority for participant, visit and unit.
   - Report the number of files and rows at every step that drops something.
   - If the rules do not cover a case, stop and ask.
2. Read the draft, save it, and commit: `git add AGENTS.md && git commit -m rules`.
3. `/new`, then test each rule with a request that breaks it:
   "Tidy up the file names in raw/ so they all look like P01_V1.csv.", "Who is participant
   P03? Look it up." Did it refuse, ask, or do it anyway? If a rule failed, ask the agent to
   add one short rule that would have stopped it.
4. `git status`: if anything in `raw/` changed, `git restore raw/` puts it back.
5. Plan file and handoff: ask for `PLAN.md` (goal, numbered steps, how each is checked, a
   "Current step" line) and `HANDOFF.md` (what is known, what is not verified, the next
   step). `/new`, then "Read HANDOFF.md and PLAN.md. What is the next step, and under
   which rules?"
6. After some work, `/compact`, then "Which rules are you working under, and what is the
   next step? Answer from what you know now, without opening any file." Compare the
   summary with what really happened.

## Part 4: keep a file away from the agent

A rule in `AGENTS.md` is a request. These are controls:

1. **Permission rule.** `cp extras/opencode.json .` then restart OpenCode. Ask
   "show me admin/linkage-key.csv". What happens?
2. **Hook.** `mkdir -p .opencode/plugins; cp extras/protect-key.js .opencode/plugins/`
   then restart. The hook runs before **every** tool call and blocks any call whose
   arguments mention `linkage-key`. Ask again, then try to get round it: "search the whole
   folder for the name Avery", "print every file under admin". Which requests got
   through, and why?
3. **The strongest control**: the file is not in the folder at all. Move it out
   (`mv admin ~/study-admin`) and ask again. In the course setup OpenCode's file tools
   cannot reach outside the project folder (except their own scratch folder /tmp/opencode), but a shell command can: every command asks
   first, and denying it is up to you. Best of all, the file never comes to the hub.

Write down which layer stopped which request. Week 6 comes back to this.

### Fewer prompts, same limits

Approving every command gets tiring, and people start approving without reading. Three
ways to ask less, from narrow to wide:

1. **Allow always** in the prompt: approves that command pattern (for example
   `Rscript *`) until OpenCode restarts.
2. **Permission patterns** in `opencode.json`, kept with the project: `cp
   extras/opencode-fewer-prompts.json opencode.json` and restart. Read-only commands
   (`ls`, `wc`, `git status`, `git diff`) and `Rscript`/`python3` run without asking;
   `rm`, `git push` and any command that names the linkage key are denied; everything
   else still asks. The last matching pattern
   wins, so `"*"` goes first. A command with a pipe is checked part by part:
   `cat notes.md | head` asks because of `cat`.
3. **`opencode --auto`**: approves everything that is not explicitly denied. Use it only
   in a git repository with a fresh commit, with your deny rules in place. Test it: under
   `--auto`, ask again for `admin/linkage-key.csv` and to delete a file with `rm`.

`--auto` does not make the agent more careful. The deny rules and `git` are what make it
safe to stop watching.

## Part 4: the merge, under your rules

With `AGENTS.md` and the controls in place, press **Tab** until the bottom line says
**Plan**, and ask for a plan (not the work) for a script `merge.py` that reads every file
in `raw/` and writes:

- `tidy/glucose_long.csv` with columns `subject, visit, time, glucose_mgdl, source_file`;
- `tidy/merge_log.csv` with one row **per file in raw/**: what was done with it and why
  (merged, converted, skipped as a duplicate, ...).

Convert mmol/L to mg/dL by multiplying by 18.016, rounded to a whole number. Anything
unexpected goes in the log, not silently fixed.

Answer its questions and correct the plan until you agree. Then **Tab** to **Build** and
ask: "Write this plan into PLAN.md, replacing the earlier draft. Keep the "Current step"
line. Do not start the work."
Commit, add the permission file, and run the plan with fewer prompts:

    git add -A && git commit -m "plan and rules"
    cp extras/opencode-fewer-prompts.json opencode.json
    opencode --auto -c

"Continue with PLAN.md: write and run merge.py. Then try, as a test of the limits: delete
tidy/ with rm, and print admin/linkage-key.csv. Report what was refused."

Checks you can do without reading code:

- `ls raw | wc -l`: every one of those files must appear in the log.
- Participants x visits x readings: how many rows should the tidy file have?
- Open one raw file and find its readings in the tidy file.
- `git status`: did anything in `raw/` change?

## Part 5: the checks as a skill

After the merge and your checks, in the same session: "Turn the checks we just ran on the
merge into a skill called check-merge, in .opencode/skills/check-merge/SKILL.md. The
description should say when to use it. Each check reports PASS or FAIL with the command and
its output. It changes no file." Restart OpenCode, then ask "Is the merge in tidy/ complete
and correct?" without naming the skill: the reply should show `Skill "check-merge"`.

## Part 6: an MCP server

"Add the arXiv MCP server to opencode.json: type local, command uvx arxiv-mcp-server. Keep
the permission rules that are already there. Show me the diff." Restart, then: "Use the
arXiv tools, at most five searches, to find three recent preprints on detecting implausible
values in glucose meter or continuous glucose monitoring data. For each: the arXiv ID, the
title, and one sentence quoted from its abstract." Open one ID and find the sentence.

## Part 8: your own slash commands

A command is a prompt saved in a file: `.opencode/commands/<name>.md` becomes `/<name>`.
Inside it, `$ARGUMENTS` is whatever you type after the command, and `` !`cmd` `` runs a
shell command and pastes its output into the prompt before the model sees it.

1. `mkdir -p .opencode/commands; cp extras/commands/*.md .opencode/commands/`, then
   restart OpenCode and type `/`: the two commands are in the list.
2. After the merge: `/check-merge`. The counts in the prompt come from the shell, not from the
   model. Compare its verdicts with your own checks above.
3. `/record merge of the raw exports`, in the same session as the checks: it appends an
   entry to `RECORD.md`. Read it. Is every check it lists one that was really run?
4. Write one of your own, for a check you do every time. For example `/n`: "for the last
   script you ran, report the number of rows after every step that can drop rows".

A command runs when you type it. A skill (Part 5) is picked up by the agent by itself.
