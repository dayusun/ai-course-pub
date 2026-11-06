import pytest

from glucose_tools import flag_implausible, parse_filename, time_in_range, to_mgdl


# item 1
def test_to_mgdl_converts_mmol():
    assert to_mgdl(6.1, "mmol/L") == 109.9
    assert to_mgdl(5, "MMOL/L") == 90.1


def test_to_mgdl_keeps_mgdl():
    assert to_mgdl(110, "mg/dL") == 110.0


def test_to_mgdl_rejects_unknown_unit():
    with pytest.raises(ValueError):
        to_mgdl(110, "g/L")


# item 2
@pytest.mark.parametrize("name, expected", [
    ("P04_V1.csv", ("P04", 1)),
    ("p04-visit1.CSV", ("P04", 1)),
    ("Subj 04 V2.csv", ("P04", 2)),
    ("Subj 4 V2.csv", ("P04", 2)),
    ("P11_visit_2.csv", ("P11", 2)),
    ("p07v2.csv", ("P07", 2)),
    ("P04_V1 (1).csv", ("P04", 1)),
])
def test_parse_filename_styles(name, expected):
    assert parse_filename(name) == expected


def test_parse_filename_rejects_other_files():
    with pytest.raises(ValueError):
        parse_filename("notes.txt")


# item 3
def test_flag_implausible():
    assert flag_implausible([15, 20, 110, 600, 601, None]) == [True, False, False, False, True, False]


def test_flag_implausible_custom_limits():
    assert flag_implausible([39, 40, 400, 401], low=40, high=400) == [True, False, False, True]


# item 4
def test_time_in_range_percent():
    assert time_in_range([65, 70, 120, 180, 181, None]) == 60.0


def test_time_in_range_rounds():
    assert time_in_range([100, 100, 200]) == 66.7


def test_time_in_range_no_readings():
    assert time_in_range([]) is None
    assert time_in_range([None, None]) is None
