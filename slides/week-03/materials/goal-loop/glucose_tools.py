"""Helpers for the glucose-meter exports of the glucose study, built one PLAN.md item at a time."""


def to_mgdl(value, unit):
    raise NotImplementedError("PLAN.md item 1")


def parse_filename(name):
    raise NotImplementedError("PLAN.md item 2")


def flag_implausible(values, low=20, high=600):
    raise NotImplementedError("PLAN.md item 3")


def time_in_range(values, low=70, high=180):
    raise NotImplementedError("PLAN.md item 4")
