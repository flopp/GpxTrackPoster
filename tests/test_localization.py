"""
Several tests for Localization
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import locale
import unittest

from gpxtrackposter.localization import localized_day_of_week_name


class TestCase(unittest.TestCase):
    """
    Test class for Localization
    """

    def test_localized_with_invalid_raises_exception(self) -> None:
        """method with invalid value returns False"""
        invalid_days_of_week = [-1, 7]
        for invalid_day in invalid_days_of_week:
            with self.subTest(f"{invalid_day}"):
                with self.assertRaises(AssertionError):
                    self.assertFalse(localized_day_of_week_name(invalid_day, True))
                    self.assertFalse(localized_day_of_week_name(invalid_day, False))

    def test_localized_returns_expected_value(self) -> None:
        """method with valid values returns expected value"""
        locale.setlocale(category=locale.LC_ALL, locale=["de_DE", "UTF-8"])
        self.assertEqual("Montag", localized_day_of_week_name(0, False))
        self.assertEqual("Samstag", localized_day_of_week_name(5, False))
        self.assertEqual("Sonntag", localized_day_of_week_name(6, False))
        self.assertEqual("M", localized_day_of_week_name(0, True))
        self.assertEqual("S", localized_day_of_week_name(5, True))
        self.assertEqual("S", localized_day_of_week_name(6, True))
        locale.setlocale(category=locale.LC_ALL, locale=["en_US", "UTF-8"])
        self.assertEqual("Monday", localized_day_of_week_name(0, False))
        self.assertEqual("Saturday", localized_day_of_week_name(5, False))
        self.assertEqual("Sunday", localized_day_of_week_name(6, False))
        self.assertEqual("M", localized_day_of_week_name(0, True))
        self.assertEqual("S", localized_day_of_week_name(5, True))
        self.assertEqual("S", localized_day_of_week_name(6, True))
        locale.setlocale(category=locale.LC_ALL, locale=["zh_CN", "UTF-8"])
        self.assertEqual("星期一", localized_day_of_week_name(0, False))
        self.assertEqual("星期六", localized_day_of_week_name(5, False))
        self.assertEqual("星期日", localized_day_of_week_name(6, False))
        self.assertEqual("一", localized_day_of_week_name(0, True))
        self.assertEqual("六", localized_day_of_week_name(5, True))
        self.assertEqual("日", localized_day_of_week_name(6, True))


if __name__ == "__main__":
    unittest.main()
