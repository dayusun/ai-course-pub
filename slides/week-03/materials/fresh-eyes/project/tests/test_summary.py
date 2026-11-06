from glucose_summary import read_rows


def test_read_rows_reads_missing_as_none(tmp_path):
    f = tmp_path / "r.csv"
    f.write_text("participant,visit,glucose,unit\nP01,1,,mg/dL\nP01,1,99,mg/dL\n")
    rows = read_rows(f)
    assert [r["glucose"] for r in rows] == [None, 99.0]
