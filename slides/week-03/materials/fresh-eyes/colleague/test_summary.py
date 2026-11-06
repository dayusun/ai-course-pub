from glucose_summary import mean_per_participant, read_rows


def test_read_rows_reads_missing_as_none(tmp_path):
    f = tmp_path / "r.csv"
    f.write_text("participant,visit,glucose,unit\nP01,1,,mg/dL\nP01,1,99,mg/dL\n")
    rows = read_rows(f)
    assert [r["glucose"] for r in rows] == [None, 99.0]


def test_mean_per_participant():
    rows = [
        {"participant": "P01", "visit": 1, "glucose": 100.0, "unit": "mg/dL"},
        {"participant": "P01", "visit": 2, "glucose": 120.0, "unit": "mg/dL"},
    ]
    assert mean_per_participant(rows)["P01"]["mean"] == 110.0
