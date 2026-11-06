---
description: Check tidy/ against raw/ (file count, rows, units); changes nothing
---
Counts taken from the shell just now:

- files in raw/: !`ls raw | wc -l`
- lines in tidy/glucose_long.csv, header included: !`wc -l < tidy/glucose_long.csv`
- lines in tidy/merge_log.csv, header included: !`wc -l < tidy/merge_log.csv`
- smallest and largest glucose_mgdl: !`python3 -c "import csv; v=[float(r['glucose_mgdl']) for r in csv.DictReader(open('tidy/glucose_long.csv'))]; print(min(v), max(v))"`

Check, and report each as PASS or FAIL with the numbers:

1. The log has one row per file in raw/.
2. The tidy file has 8 readings for every subject and visit it contains, and every
   subject-visit appears once (duplicates skipped).
3. Every glucose value is plausible in mg/dL (about 40 to 400); a value under 30 suggests
   an unconverted mmol/L file.

Do not change any file. If a count cannot be explained, say so.
