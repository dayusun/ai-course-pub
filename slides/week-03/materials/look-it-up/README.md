# More practice: looking things up, with sources

The agent can fetch web pages and, if you turn it on, search the web. Every page it reads
is a tool call you can see, approve and check, which a chatbot answer does not give you.

Nothing from a study goes into a query: a search term leaves the hub (Week 1, classifying
data). Start with `git init` in this folder.

## Step 1: check a reference list (fetch)

`references-to-check.md` comes from a draft methods section. Some entries may be wrong.

1. **Plan.** Ask how it would check each reference **without relying on memory**. A good
   plan names a source per entry: the DOI at `https://api.crossref.org/works/<doi>`, or a
   PubMed search for entries without a DOI.
2. **Build.** Ask for `reference-check.md`: one row per reference with the verdict
   (matches, which field is wrong, or not found) and **the URL it read**. OpenCode asks
   before every fetch: read each URL before you allow it.
3. **Check two rows yourself**: open the URL it cites and compare.

## Step 2: a current fact (search)

Quit OpenCode and start it with search turned on:

    OPENCODE_ENABLE_EXA=1 opencode

1. "What is the current CRAN version of the R package lme4, and when was it published?
   Give the page you read."
2. "What factor converts glucose from mmol/L to mg/dL, and why that number? Cite a
   primary source." (The glucose merge used it.)

For each answer: open the page, find the sentence, and note the date you checked. Searches
go to an outside service (Exa): the query text leaves the hub.

## A skill: turn what worked into one

A skill is a folder with a `SKILL.md`: a name, a one-line description, and the steps. The
agent sees only the descriptions until a task matches one, then loads that skill's steps.
OpenCode looks in `.opencode/skills/<name>/SKILL.md`.

1. **Build.** In the session from step 1, ask: "Turn how we just checked the references into
   a skill called `reference-check` in `.opencode/skills/reference-check/SKILL.md`: when to
   use it, the sources in order, and the table it produces." Read the draft. Cut what is
   vague; keep the sources, the order, and the table format. Compare it with
   `extras/skills/reference-check/SKILL.md`, which also ships a small script,
   `check_doi.py`, so the Crossref lookup runs the same way every time.
2. **Use.** Restart OpenCode, `/new`, then: "Check the references in `draft-2.md`." Do not
   name the skill. The session should show the skill being loaded before any fetch, and the
   output should follow the skill's table.
3. **Check.** `draft-2.md` has different errors from the first list. Check two of the
   flagged rows yourself.

A slash command (Part 8) runs when you type it. A skill is picked by the agent from its
description, so the description decides when it is used: try a request that should trigger
it and one that should not.

## MCP: a tool from a server

An MCP server is a program that offers tools to the agent. OpenCode starts it from
`opencode.json` and lists its tools next to the built-in ones.

1. `cp extras/opencode-mcp.json opencode.json`, restart OpenCode. The first start downloads
   the servers (a minute). `opencode mcp list` in a terminal shows whether they connected.
2. **An existing server, arXiv.** "Find three preprints from the last two years on
   diagnostics for multiple imputation, and give their arXiv IDs." Then open one of the IDs
   yourself.
3. **A server you can read.** `extras/mcp/crossref_server.py` is about 30 lines: one tool,
   `lookup_doi`, that asks Crossref for a DOI's record. Read it. Then redo two rows of step 1
   with "use the crossref tool". Compare with the fetch in step 1: one tool call that
   returns fields instead of a whole page, and the same call every time.
4. What would you want as a tool for your own work? A lab database, a REDCap export, a
   codebook? The server is the place to put the access rules, not the prompt.
