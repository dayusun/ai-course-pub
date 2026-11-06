# Starter project: cleaning home blood-pressure readings

Synthetic teaching data; no real participants.

`cleaning.py` keeps plausible systolic readings (70-250 mmHg) and reports the mean of the
last three readings in day order. One of its functions has a bug.

## Before you use an agent

Open `example.csv`. By hand, drop the implausible reading, then compute the mean systolic
pressure of the last three remaining readings (in day order). Write down your answer.

## Run

    python run.py example.csv     # prints the cleaned rows and the mean
    python -m unittest -v         # runs the three tests

There is no Makefile: `make test` does not work here.
