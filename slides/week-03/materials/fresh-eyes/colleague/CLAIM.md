# The colleague's report

Added `mean_per_participant(rows)`. It works in mg/dL, leaves out implausible readings
(outside 20-600) and missing ones, and reports n for each participant. Added a test;
`python3 -m pytest -q` passes. Output on `data/readings.csv`:

    P01  mean  114.9 mg/dL  (n = 8)
    P02  mean   99.2 mg/dL  (n = 8)
    P03  mean  129.5 mg/dL  (n = 8)
    P04  mean  159.0 mg/dL  (n = 8)

Ready to commit.
