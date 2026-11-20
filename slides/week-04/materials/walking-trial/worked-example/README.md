# Week 4 worked example: raw material

Run on 21 October 2026 with OpenCode 1.19.3 in the course hub image
(`class-hub/student:2026.10`) and the course's default model, `nrp/qwen3-small`
(Qwen3.8-27B on NRP). Non-interactive: `opencode run --auto` inside a throwaway
container, with only the synthetic data in the folder.

- `runs/A_*`: plain prompt (`prompt.txt`), no `AGENTS.md`.
- `runs/B_*`: `AGENTS.md` (this folder) plus a short prompt.
- `runs/leak_*`: the first attempt, where `tests/check_results.py` sat inside the agent's
  folder and the agent read the expected values before computing.
- `verifier/check_results.py`: the expected values, written before the runs and run by
  us after each agent finished (`verifier.txt` in each run).

All data are synthetic (`../cohort.csv`).
