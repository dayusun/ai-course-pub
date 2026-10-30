# Task 118: live demos for the Week 2 deck (NRP models, saved raw output)

Folder: /mnt/fanxiangssd/ai-docker/prompts/118-week02-demos (create it). Use the NRP API
(https://ellm.nrp-nautilus.io/v1). The key is NRP_LLM_API_KEY from the environment: never
print it, never save it to a file.

Models: nrp/qwen3-small (Qwen3.8-27B) and nrp/glm-5 (GLM-5.3). Use qwen3-vl for vision.
Run `check-models`-style calls first and record which underlying model each alias serves.

For every demo, save:
- the exact prompts (prompts/),
- the raw JSON responses (raw/),
- a short results.md: model ids, date and time, settings, the numbers.

Use temperature 0 unless a demo says otherwise. Keep everything synthetic or public. No
GPU work is needed; leave ComfyUI alone.

1. **Lost in the middle.**
   - Build a long synthetic document, about 30k tokens, of plausible but irrelevant
     clinical-trial prose. Use public-domain or generated text; no copyrighted text.
   - Insert one "needle" sentence ("The trial's primary outcome was measured at week 37.")
     at 5%, 50% and 95% depth.
   - Ask "At which week was the primary outcome measured? Answer with the number." 5 trials
     per position per model, varying the filler seed.
   - Report accuracy per position per model, and make a PNG bar chart (matplotlib, light
     theme, large fonts): needle-position.png.
2. **Reasoning effort.**
   - Take one multi-step biostatistics question with a known answer. For example: a
     two-sample comparison where the student must compute a pooled SD then a 95% CI. Give
     the numbers and the correct answer in results.md.
   - Run it on glm-5 and qwen3-small with reasoning off or low versus high, if the API
     supports a reasoning setting (find out which parameter works on NRP; if none, say so).
   - Record the answer, correctness, latency, and completion and reasoning tokens.
3. **Stateless.** Call 1: "My name is Dana and my study has 412 participants." Call 2, a
   separate request: "How many participants are in my study?" Save both answers. Then repeat
   with the history resent in call 2.
4. **Fabricated references.**
   - Ask qwen3-small and glm-5, with no search: "List 8 peer-reviewed papers (authors, year,
     title, journal, DOI) on text-message reminders for medication adherence."
   - Check each reference against Crossref (api.crossref.org/works?query.bibliographic=...,
     and resolve each DOI). Classify each as real-and-matching, real-but-wrong-details, or
     not found.
   - Report counts per model in a table. Do not paste long abstracts.
5. **RAG miss.**
   - Using the three synthetic papers in /mnt/fanxiangssd/ai-docker/prompts/115-student-hub/
     (or recreate: WALK-1, WALK-2, STEP-HTN from the Week 2 materials; ask the deck session
     if you cannot find them), build a tiny retrieval: split into chunks and use simple
     keyword or embedding search with qwen3-embedding.
   - Ask "Did any trial measure ambulatory blood pressure?" with top-k = 1 and with top-k = 3.
   - Show which chunks were retrieved and whether the answer is right.
6. **Vision.**
   - Give qwen3-vl the image
     /mnt/fanxiangssd/ai-docker/prompts/118-week02-demos/broken-figure.png. The deck session
     will copy it there; if missing, wait and ask.
   - Prompt: "Describe this chart: the groups, their values, and anything misleading."
   - Save the answer and note whether it catches the truncated axis (one bar invisible) and
     reports the right labels.

Report a short summary table of all six demos with the headline numbers, and list anything
that did not work.
