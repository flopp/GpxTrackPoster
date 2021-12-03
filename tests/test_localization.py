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
            with self.assertRaises(AssertionError):
                self.assertFalse(localized_day_of_week_name(invalid_day, True))
                self.assertFalse(localized_day_of_week_name(invalid_day, False))

    def test_localized_returns_expected_value(self) -> None:
        """method with valid values returns expected value"""
        locale.setlocale(locale.LC_ALL, "de_DE")
        self.assertEqual(localized_day_of_week_name(0, False), "Montag")
        self.assertEqual(localized_day_of_week_name(5, False), "Samstag")
        self.assertEqual(localized_day_of_week_name(6, False), "Sonntag")
        self.assertEqual(localized_day_of_week_name(0, True), "M")
        self.assertEqual(localized_day_of_week_name(5, True), "S")
        self.assertEqual(localized_day_of_week_name(6, True), "S")
        locale.setlocale(locale.LC_ALL, "en_GB")
        self.assertEqual(localized_day_of_week_name(0, False), "Monday")
        self.assertEqual(localized_day_of_week_name(5, False), "Saturday")
        self.assertEqual(localized_day_of_week_name(6, False), "Sunday")
        self.assertEqual(localized_day_of_week_name(0, True), "M")
        self.assertEqual(localized_day_of_week_name(5, True), "S")
        self.assertEqual(localized_day_of_week_name(6, True), "S")
        locale.setlocale(locale.LC_ALL, "zh_CN")
        self.assertEqual(localized_day_of_week_name(0, False), "星期一")
        self.assertEqual(localized_day_of_week_name(5, False), "星期六")
        self.assertEqual(localized_day_of_week_name(6, False), "星期日")
        self.assertEqual(localized_day_of_week_name(0, True), "一")
        self.assertEqual(localized_day_of_week_name(5, True), "六")
        self.assertEqual(localized_day_of_week_name(6, True), "日")


if __name__ == "__main__":
    unittest.main()
