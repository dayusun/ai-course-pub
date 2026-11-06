---
name: reference-check
description: Check references against Crossref and PubMed and report, per reference, whether it matches, which field is wrong, or that no record exists. Use when asked to check, verify or audit citations or a reference list.
---

# Reference check

Never judge a reference from memory. Every verdict comes from a record read in this session.

## Steps

1. Number the references as they appear in the file.
2. With a DOI: `python3 .opencode/skills/reference-check/check_doi.py <doi>`. It prints the
   Crossref record, or `NOT FOUND` with the URL it tried.
3. Without a DOI, or when the DOI is not found: search Crossref by citation,
   `https://api.crossref.org/works?query.bibliographic=<title and first author>&rows=3`, then
   PubMed, `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<title>[ti]`.
   A record counts as a match only if the title matches, not just the topic.
4. Compare, field by field: authors and their order, title, journal, year, volume, pages.
   A subtitle missing from the record is a note, not an error.

## Output

Write `reference-check.md` with one row per reference:

| # | First author, year | Verdict | Wrong field: given -> record | Source read |
|---|---|---|---|---|

Verdict is one of `matches`, `wrong field`, `not found`. "Source read" is the URL or the
command, so a person can repeat the check. Below the table, list the references that need
the author's attention, one line each. Change no other file.
