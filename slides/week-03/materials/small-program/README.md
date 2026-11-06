# More practice: a small research tool, from scratch

Pick one. Both follow the same order: a spec you write, Plan, tests or known answers before
code, Build in small commits, then use it on real input. `git init` in this folder first.

## Option A: a codebook from any CSV (command line)

The spec, to paste and adjust:

> Write `codebook.py`. `python3 codebook.py data.csv` writes `codebook.md`: one section per
> column with its type (number or text), the number of empty cells, values that look like
> missing codes (-99, -9, 999, 9999, "NA", "."), and the range (numbers) or the levels with
> counts (text, at most 10). Standard library only. Do not change the input file.

1. **Plan** (Tab): ask for the plan and the test cases. Do they cover an empty cell, a -99,
   a column that is all text, a file with one row?
2. **Tests first**: "Write `test_codebook.py` with pytest from the spec. Do not write
   `codebook.py` yet." Run `pytest`: every test fails. Commit.
3. **Build**: "Now write `codebook.py` until the tests pass." Run `pytest` yourself. Commit.
4. **Use**: `python3 codebook.py ../inherited-analysis/survey.csv`. Compare `codebook.md`
   with `checks.md`. It should have found what the inherited script missed (`inherited-analysis/`).
5. Run it on a CSV of your own (no protected data).

## Option B: a sample-size calculator (web page)

> Write `index.html`, a single page with no libraries: inputs for the standardized effect
> size d, alpha (two-sided) and power; output the sample size per group for comparing two
> means with a t-test, rounded up, and the formula used.

1. **Plan**: ask which formula it will use, and how it handles the t distribution.
2. **Known answers first**: write down what R says, from `checks.md`. These are your tests.
3. **Build**, then serve the page: `python3 -m http.server 8000` in a terminal, and open
   `https://<hub address>/user/<your name>/proxy/8000/` in the browser.
4. **Check** against the known answers. If it is off by one, ask why, and decide which
   answer you want (Plan first).

Both options: copy `../glucose-study/.opencode/commands/record.md` into `.opencode/commands/`
(after Part 8), end with `/record`, and look at `git log`.
