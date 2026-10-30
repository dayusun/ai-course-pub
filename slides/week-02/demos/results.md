# Week 2 live demos: results (NRP, 2026-10-20)

All calls went to `https://ellm.nrp-nautilus.io/v1` between 20:31 and 20:45 EDT (00:31–00:45 UTC on
2026-10-21), temperature 0. The key came from `NRP_LLM_API_KEY` in the environment and appears in no file
here (checked: 0 matches). Exact prompts are in `prompts/`, every request and raw response in `raw/` (88
files), the code in `scripts/`. Everything is synthetic or public.

## Summary

| Demo | Headline |
|---|---|
| 1. Lost in the middle | 30/30 correct: 5/5 at 5%, 50% and 95% depth for both models at about 27–28k tokens. No position effect at this length with one unique needle (`needle-position.png`) |
| 2. Reasoning effort | All 17 graded answers correct (pooled SD 11.10, CI 0.27 to 12.33); glm-5 "thinking off" failed 1 of 3 (ran out of tokens). Thinking costs time: qwen3-small 10 s off vs 71–103 s at `xhigh`; glm-5 8–12 s low vs 18–24 s high |
| 3. Stateless | Without history both models said they had no information; with the history resent both answered "412 participants, Dana" |
| 4. Fabricated references | qwen3-small: 0 DOIs given, 4 distinct titles among 8 entries, 0/8 found. glm-5: 4 real and matching, 3 real but wrong details, 1 not found |
| 5. RAG miss | Embedding search: correct at top-1 and top-3 (STEP-HTN ranked first). Keyword search: top-1 retrieved WALK-1 (office SBP) and the answer was "no mention of ambulatory blood pressure"; top-3 correct |
| 6. Vision | qwen3-vl gave both labels and values (4.7%, 9.3%), named the y-axis starting at 5, the invisible Usual care bar and the exaggerated difference |

## 0. Which model each alias served

| Alias | Served model (`model` field of the response) | Check |
|---|---|---|
| `qwen3-small` | `Qwen/Qwen3.8-27B` | HTTP 200, 0.9 s |
| `glm-5` | `Inferact/GLM-5.3-NVFP4` | HTTP 200, 0.7 s |
| `qwen3-vl` | `Qwen/Qwen3.8-Flash-Next-FP8` | HTTP 200, 5.5 s |
| `qwen3-embedding` | `Qwen/Qwen3-VL-Embedding-8B` (4096 dimensions) | HTTP 200 |

## 1. Lost in the middle

- Document: generated trial-operations prose (site visits, monitoring, shipping, consent), about 21,500
  words, which is 28.0k prompt tokens on qwen3-small and 26.6k on glm-5. Five filler seeds (1–5). The filler
  never contains the word "outcome" or the number 37, but it does mention other visit weeks. Example:
  `prompts/d1_example_doc_seed1_depth50.txt`.
- Needle: "The trial's primary outcome was measured at week 37.", inserted between sentences at 5%, 50% or
  95% of the sentences. Question appended after the document: "At which week was the primary outcome
  measured? Answer with the number."
- Settings: temperature 0, `reasoning_effort: low`, `max_tokens` 2048. Correct = the answer contains 37.

| Model | 5% depth | 50% depth | 95% depth | Latency per call |
|---|---|---|---|---|
| qwen3-small | 5/5 | 5/5 | 5/5 | 9.7–18.1 s |
| glm-5 | 5/5 | 5/5 | 5/5 | 6.2–23.4 s |

No position effect at this length with a single, unique needle. A visible effect would likely need a much
longer document, several similar distractor sentences, or a question that needs two facts combined; none of
those was run.

## 2. Reasoning effort

Question (`prompts/d2_reasoning.txt`): Group A n = 25, mean 132.4 mmHg, SD 10.2; group B n = 30, mean
126.1 mmHg, SD 11.8; equal variances; pooled SD and 95% CI for A minus B with the t distribution; final line
`ANSWER: pooled_sd=<x>; ci=(<lo>, <hi>)`.

Correct answer (scipy): pooled SD = sqrt((24 × 10.2² + 29 × 11.8²) / 53) = **11.10**; SE = 11.10 ×
sqrt(1/25 + 1/30) = 3.007; t(0.975, 53) = 2.006; difference 6.30; **95% CI 0.27 to 12.33**. (With z = 1.96
instead of t: 0.41 to 12.19.) Graded correct when all three numbers are within 0.02.

Reasoning controls that work on NRP (probe in `raw/d2_probe_*.json`):

| Model | Off | Low | High |
|---|---|---|---|
| qwen3-small | `chat_template_kwargs: {enable_thinking: false}` (0 reasoning tokens) | `reasoning_effort: "low"` | `reasoning_effort: "xhigh"` (the default; `"high"` returns HTTP 400 "Supported types are xhigh (default), medium, and low") |
| glm-5 | `enable_thinking: false` stops the separate reasoning channel, but the model then works the problem out in the visible answer | `reasoning_effort: "low"` | `reasoning_effort: "high"` |

Three repeats per cell, temperature 0, `max_tokens` 16384:

| Model | Setting | Correct | Latency (s) | Completion tokens | Reasoning tokens |
|---|---|---|---|---|---|
| qwen3-small | off | 3/3 | 9.8, 10.1, 10.2 | 1030, 1030, 1030 | 0, 0, 0 |
| qwen3-small | low | 3/3 | 22.2, 22.3, 23.2 | 2362, 2374, 2506 | 1940, 1940, 2085 |
| qwen3-small | high (xhigh) | 3/3 | 70.7, 98.9, 103.0 | 3467, 5117, 5329 | 3438, 5088, 5300 |
| glm-5 | off | 2/3 | 45.9, 79.9, 358.2 | 1967, 3360, 16384 | 0, 0, 0 |
| glm-5 | low | 3/3 | 8.4, 9.2, 11.9 | 354, 358, 450 | 157, 157, 222 |
| glm-5 | high | 3/3 | 18.2, 18.2, 23.8 | 696, 742, 941 | 330, 353, 583 |

The failed glm-5 "off" run did long-hand arithmetic in the answer until it hit the 16,384-token limit
(`finish_reason: length`, no ANSWER line). Token counts vary between repeats even at temperature 0.

## 3. Stateless

Settings: temperature 0, `reasoning_effort: low`. Full answers in `raw/d3_summary.json`.

| Model | Call 2 alone ("How many participants are in my study?") | Call 2 with call 1 and its reply resent |
|---|---|---|
| qwen3-small | "I don't have any information about your study. I don't have access to your documents, research data, or any personal details about your work." | "Your study has **412 participants**, Dana." |
| glm-5 | "I don't have any information about your study — this is the start of our conversation, and you haven't shared any details yet." | "Your study has **412 participants**, Dana." |

## 4. Fabricated references

Prompt (`prompts/d4_references.txt`), no search tools, temperature 0, `reasoning_effort: low`. A second call
(qwen3-small, thinking off, `prompts/d4_extract_template.txt`) converted each list to JSON; I compared the
JSON with the raw answers by eye. Each reference was checked with Crossref `works/{doi}`, Crossref
`works?query.bibliographic=<title + authors>` (best title similarity ≥ 0.9 counts as found) and a HEAD request
to `doi.org`. Classes: **real-and-matching** = the DOI resolves to this title with the same year and first
author; **real-but-wrong-details** = the title exists but the DOI, year, author or journal is wrong;
**not-found** = no Crossref match for either.

| Model | Real and matching | Real, wrong details | Not found | DOIs given |
|---|---|---|---|---|
| qwen3-small | 0 | 0 | 8 | 0 |
| glm-5 | 4 | 3 | 1 | 8 |

- qwen3-small declined to give DOIs ("I am **not** providing DOIs because I would be guessing"), noticed it
  was repeating entries, and listed 8 rows with only 4 distinct titles (e.g. "Text messaging for medication
  adherence: a systematic review" under two author names). None matched Crossref (best title similarity
  0.50–0.65).
- glm-5, real and matching: Vervloet 2012 (JAMIA), Thakkar 2016 (JAMA Intern Med), Pop-Eleches 2011 (AIDS),
  Lester 2010 (Lancet).
- glm-5, real but wrong details: Mbuagbaw 2012 CAMPS trial (real, but in PLoS ONE, 10.1371/journal.pone.0046909;
  the given JAIDS DOI does not exist); Wald one-way vs two-way texting (real, Am J Med **2015**,
  10.1016/j.amjmed.2015.05.035; the given DOI resolves to an unrelated paper on organ donation); "mHealth SMS
  text messaging interventions and to promote medication adherence" given as Fisher 2006, JMIR mHealth (the
  title is real, but by DeKoekkoek et al. 2015 in J Clin Nurs, 10.1111/jocn.12918; the given DOI does not exist).
- glm-5, not found: Kannry 2017, "Use of a text messaging platform to enhance adherence to weight loss..." (DOI
  10.2196/mhealth.6709 does not exist; off-topic as well).

## 5. RAG miss

Corpus: `paper-walk1.md`, `paper-walk2.md`, `paper-stephtn.md` (synthetic), one chunk per "p. N." paragraph
(11 chunks, no titles attached). Question: "Did any trial measure ambulatory blood pressure?" Correct answer:
yes, STEP-HTN (primary outcome 24-hour ambulatory SBP at 24 weeks). The answer model was qwen3-small
(`reasoning_effort: low`) with `prompts/d5_template.txt` ("Answer the question using only the excerpts below.
If the excerpts do not contain the answer, say so.").

Retrievers: cosine similarity on `qwen3-embedding` vectors, and keyword overlap (shared words with the
question, ignoring "did, any, trial, measure"; ties broken by document order).

| Retriever | k | Retrieved | Answer | Right? |
|---|---|---|---|---|
| embedding | 1 | stephtn p.5 (cos 0.715) | Yes, STEP-HTN: 24-hour ambulatory SBP | yes |
| embedding | 3 | stephtn p.5, stephtn p.7, walk2 p.4 | Yes, STEP-HTN; WALK-2 used home SBP | yes |
| keyword | 1 | walk1 p.5 ("office systolic blood pressure", 2 shared words) | "there is no mention of ambulatory blood pressure ... The excerpts do not contain enough information" | **no** |
| keyword | 3 | walk1 p.5, stephtn p.5, stephtn p.7 | Yes, STEP-HTN (called "The Stephenson trial", a name invented from the chunk id `stephtn`) | yes, with a wrong trial name |

The keyword miss happens because STEP-HTN writes "ambulatory SBP" and never "blood pressure", while WALK-1
spells out "systolic blood pressure". The embedding retriever ranked the STEP-HTN chunks first.

## 6. Vision

`qwen3-vl` (served `Qwen/Qwen3.8-Flash-Next-FP8`), temperature 0, default reasoning; 126 s, 600 prompt tokens,
1,301 completion tokens of which 832 reasoning. Prompt: "Describe this chart: the groups, their values, and
anything misleading." Full answer: `raw/d6_qwen3-vl.json` (the image payload is omitted from the saved request).

| Check | Result |
|---|---|
| Labels | Usual care 4.7%, Walking 9.3%: correct |
| Truncated axis | "The chart's vertical axis does **not** start at 0; it starts at **5** and runs to 12": caught |
| Invisible bar | "The 'Usual care' bar is invisible. Because 4.7% lies *below* the axis floor of 5, the bar is clipped out of the plot area entirely": caught |
| Other | Notes the exaggerated difference (true ratio about 2:1) and the 4.7% label overlapping the category name |

## What did not work or differed

- `reasoning_effort: "high"` is rejected for qwen3-small (HTTP 400); its top level is `xhigh`, which is also
  the default.
- glm-5 has no clean "off": `enable_thinking: false` moves the reasoning into the answer, which was slower than
  `low` and failed once by running out of tokens.
- The needle test showed no lost-in-the-middle effect at about 27–28k tokens.
- qwen3-small did not produce DOIs, so its references could only be checked by title; it also returned 8 rows
  with only 4 distinct titles.
- qwen3-vl took 126 s for one image.
