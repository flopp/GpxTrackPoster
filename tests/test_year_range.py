"""
Several tests for YearRange
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from datetime import datetime
import unittest

from gpxtrackposter.year_range import YearRange


class TestCase(unittest.TestCase):
    """
    Test class for YearRange
    """

    def test_init_returns_invalid_instance(self) -> None:
        """YearRange object is initialised with None values"""
        year_range = YearRange()
        self.assertIsNone(year_range.from_year)
        self.assertIsNone(year_range.to_year)

    def test_parse_with_valid_strings_sets_values_returns_true(self) -> None:
        """parse with valid strings returns True"""
        valid_strings = [("all", None, None), ("2016", 2016, 2016), ("2018", 2018, 2018), ("2016-2018", 2016, 2018)]
        for string, from_year, to_year in valid_strings:
            with self.subTest(f"{string} -> {from_year}-{to_year}"):
                year_range = YearRange()
                self.assertTrue(year_range.parse(string))
                self.assertEqual(from_year, year_range.from_year)
                self.assertEqual(to_year, year_range.to_year)

    def test_parse_with_invalid_strings_returns_false(self) -> None:
        """parse with invalid strings returns False"""
        invalid_strings = ["20xx", "20xx-2018", "2016:2018"]
        for string in invalid_strings:
            with self.subTest(f"{string}"):
                year_range = YearRange()
                self.assertFalse(year_range.parse(string))

    def test_parse_with_wrong_order_returns_false(self) -> None:
        """parse with wrong order of years returns False"""
        invalid_string = "2018-2016"
        year_range = YearRange()
        self.assertFalse(year_range.parse(invalid_string))

    def test_clear_returns_empty_instance(self) -> None:
        """clear returns empty instance of YearRange"""
        valid_strings = ["2016", "2018", "2016-2018"]
        for string in valid_strings:
            with self.subTest(f"{string}"):
                year_range = YearRange()
                self.assertTrue(year_range.parse(string))
                self.assertIsNotNone(year_range.from_year)
                self.assertIsNotNone(year_range.to_year)
                year_range.clear()
                self.assertIsNone(year_range.from_year)
                self.assertIsNone(year_range.to_year)

    def test_add_increases_year_range(self) -> None:
        """add with higher/lower values increases YearRange"""
        valid_strings = [
            ("all", datetime(2015, 1, 1), 2015, 2015),
            ("2016", datetime(2015, 1, 1), 2015, 2016),
            ("2016", datetime(2019, 1, 1), 2016, 2019),
            ("2016-2018", datetime(2015, 1, 1), 2015, 2018),
            ("2016-2018", datetime(2019, 1, 1), 2016, 2019),
        ]
        for string, added, from_year, to_year in valid_strings:
            with self.subTest(f"{string}, {added} -> {from_year}-{to_year}"):
                year_range = YearRange()
                self.assertTrue(year_range.parse(string))
                year_range.add(added)
                self.assertEqual(from_year, year_range.from_year)
                self.assertEqual(to_year, year_range.to_year)

    def test_contains_returns_true(self) -> None:
        """contains returns True"""
        valid_strings = [
            ("all", datetime(2015, 1, 1)),
            ("2016", datetime(2016, 1, 1)),
            ("2016-2018", datetime(2016, 1, 1)),
            ("2016-2018", datetime(2017, 1, 1)),
            ("2016-2018", datetime(2018, 1, 1)),
        ]
        for string, value in valid_strings:
            with self.subTest(f"{string}, {value}"):
                year_range = YearRange()
                self.assertTrue(year_range.parse(string))
                self.assertTrue(year_range.contains(value))

    def test_contains_returns_false(self) -> None:
        """contains returns False"""
        valid_strings = [
            ("2016", datetime(2015, 1, 1)),
            ("2016", datetime(2017, 1, 1)),
            ("2016-2018", datetime(2015, 1, 1)),
            ("2016-2018", datetime(2019, 1, 1)),
        ]
        for string, value in valid_strings:
            with self.subTest(f"{string}, {value}"):
                year_range = YearRange()
                self.assertTrue(year_range.parse(string))
                self.assertFalse(year_range.contains(value))

    def test_count_with_empty_year_range_returns_zero(self) -> None:
        """count with empty year range returns 0"""
        year_range = YearRange()
        self.assertEqual(0, year_range.count())

    def test_count_returns_value(self) -> None:
        """count returns value"""
        valid_strings = [
            ("2016", 1),
            ("2016-2018", 3),
            ("2015-2019", 5),
        ]
        for string, expected_value in valid_strings:
            with self.subTest(f"{string} -> {expected_value}"):
                year_range = YearRange()
                self.assertTrue(year_range.parse(string))
                self.assertEqual(expected_value, year_range.count())

    def test_iter_with_empty_year_range_returns(self) -> None:
        """iter with empty year range returns"""
        year_range = YearRange()
        list_of_years = []
        for year in year_range.iter():
            list_of_years.append(year)
        self.assertListEqual([], list_of_years)

    def test_iter_returns_values(self) -> None:
        """iter returns YearRange values"""
        valid_strings = [
            ("2016", [2016]),
            ("2016-2018", [2016, 2017, 2018]),
            ("2015-2019", [2015, 2016, 2017, 2018, 2019]),
        ]
        for string, expected_values in valid_strings:
            with self.subTest(f"{string} -> {expected_values}"):
                year_range = YearRange()
                self.assertTrue(year_range.parse(string))
                list_of_years = []
                for year in year_range.iter():
                    list_of_years.append(year)
                self.assertListEqual(expected_values, list_of_years)


if __name__ == "__main__":
    unittest.main()
