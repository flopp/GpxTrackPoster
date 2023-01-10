"""
Several tests for Localization
"""
# Copyright 2021-2023 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import locale

import pytest

from gpxtrackposter.localization import localized_day_of_week_name


@pytest.mark.parametrize(
    "invalid_day",
    [-10, -1, 7, 10],
)
def test_localized_with_invalid_raises_exception(invalid_day: int) -> None:
    """method with invalid value returns False"""
    with pytest.raises(AssertionError):
        assert not localized_day_of_week_name(invalid_day, True)
        assert not localized_day_of_week_name(invalid_day, False)


@pytest.mark.parametrize(
    "language, locale_lang, weekday_num, short, expected",
    [
        ("german", "de_DE", 0, False, "Montag"),
        ("german", "de_DE", 5, False, "Samstag"),
        ("german", "de_DE", 6, False, "Sonntag"),
        ("german", "de_DE", 0, True, "M"),
        ("german", "de_DE", 5, True, "S"),
        ("german", "de_DE", 6, True, "S"),
        ("english", "en_US", 0, False, "Monday"),
        ("english", "en_US", 5, False, "Saturday"),
        ("english", "en_US", 6, False, "Sunday"),
        ("english", "en_US", 0, True, "M"),
        ("english", "en_US", 5, True, "S"),
        ("english", "en_US", 6, True, "S"),
        ("chinese", "zh_CN", 0, False, "星期一"),
        ("chinese", "zh_CN", 5, False, "星期六"),
        ("chinese", "zh_CN", 6, False, "星期日"),
        ("chinese", "zh_CN", 0, True, "一"),
        ("chinese", "zh_CN", 5, True, "六"),
        ("chinese", "zh_CN", 6, True, "日"),
    ],
)
def test_localized_returns_expected_value(
    language: str, locale_lang: str, weekday_num: int, short: bool, expected: str
) -> None:
    """method with valid values returns expected value"""
    print(language)
    locale.setlocale(category=locale.LC_ALL, locale=[locale_lang, "UTF-8"])
    assert expected == localized_day_of_week_name(weekday_num, short)
