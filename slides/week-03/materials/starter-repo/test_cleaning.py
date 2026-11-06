import unittest

from cleaning import clean, mean_of_last


def r(day, sbp):
    return {"id": "T", "day": day, "sbp": sbp}


class TestCleaning(unittest.TestCase):
    def test_clean_drops_implausible(self):
        rows = [{"id": "T", "day": "1", "sbp": "120"}, {"id": "T", "day": "2", "sbp": "20"}]
        self.assertEqual(clean(rows), [r(1, 120)])

    def test_mean_of_last_three(self):
        readings = [r(d, s) for d, s in [(1, 130), (2, 140), (3, 150), (4, 160), (5, 170)]]
        self.assertAlmostEqual(mean_of_last(readings, 3), 160.0)

    def test_mean_when_fewer_than_k(self):
        readings = [r(1, 120), r(2, 130)]
        self.assertAlmostEqual(mean_of_last(readings, 3), 125.0)


if __name__ == "__main__":
    unittest.main()
