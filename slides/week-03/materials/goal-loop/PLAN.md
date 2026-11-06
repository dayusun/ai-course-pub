# Plan

Work through the items in order. Tick an item (`- [x]`) only when its tests pass.

- [ ] 1. `to_mgdl(value, unit)`: "mg/dL" returns the value as a float; "mmol/L" (any case)
  multiplies by 18.016; round to 1 decimal. Any other unit raises ValueError.
- [ ] 2. `parse_filename(name)`: returns (participant, visit), e.g. ("P04", 1), for the five
  export name styles of the glucose study and for browser copies such as "P04_V1 (1).csv".
  Participant always as P plus two digits. Anything else raises ValueError.
- [ ] 3. `flag_implausible(values, low=20, high=600)`: one True/False per value, True when
  the value is below `low` or above `high`. A missing value (None) is not flagged.
- [ ] 4. `time_in_range(values, low=70, high=180)`: percent of non-missing readings with
  low <= value <= high, rounded to 1 decimal; None when there are no readings.
