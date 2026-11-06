# Week 3 hands-on folders

All data are synthetic. The slides have every step with the prompts to copy; each folder's
README has the same steps for when you continue after class. What you do not finish
carries into Week 4.

## The running project

| Folder | Part | What you do |
|---|---|---|
| `glucose-study/` | 1-6, 8-9 | open it, write `AGENTS.md`, plan and run the merge, keep the linkage key out, check the result, turn the checks into a skill, add an MCP server, slash commands, the record |
| `fresh-eyes/` | 7 | the study's summary step: a read-only reviewer subagent, and several subagents at once |
| `goal-loop/` | 8 | the merge as four functions: a goal check and a Ralph loop |

## More practice

| Folder | What you practise |
|---|---|
| `inherited-analysis/` | explain and repair an inherited R script; no programming needed |
| `starter-repo/` | fix a bug with tests, and prove the fix |
| `look-it-up/` | check references with sources, then a skill and an MCP server for it |
| `small-program/` | write a small research tool from scratch: codebook or sample-size page |
| `long-session/` | long sessions: what compaction keeps, rules in files, handoff |
| your own project | the same setup on your own work (below) |

Start each in its own folder: `cd ~/week-03/<folder>`, `git init`, `opencode`.

## Your own project

Bring a project with **no protected data** (code, public data, a draft). In a copy of it:

1. `git init` and a first commit.
2. Let the agent draft `AGENTS.md`: "Read this folder. Ask me, one question at a time, what
   you need to know to work here safely, then write AGENTS.md in under 30 lines."
3. One control that is not a request: a permission rule or a hook for the file or folder
   the agent must not touch.
4. One real task, Plan first. Record the prompt, the model, what changed (`git diff`) and how
   you checked it: copy `~/week-03/glucose-study/.opencode/commands/record.md` into the
   project's `.opencode/commands/` and run `/record`. That record is your Week 3 portfolio entry.
