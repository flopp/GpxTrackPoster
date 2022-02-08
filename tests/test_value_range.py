"""
Several tests for ValueRange
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import pytest

from gpxtrackposter.value_range import ValueRange


def test_init_returns_invalid_instance() -> None:
    """ValueRange object is initialised with None values, thus invalid"""
    value_range = ValueRange()
    assert not value_range.is_valid()


def test_from_pair_returns_instance() -> None:
    """from_pair returns instance of ValueRange"""
    value_range = ValueRange.from_pair(0.0, 0.0)
    assert value_range.is_valid()
    assert isinstance(value_range, ValueRange)


@pytest.mark.parametrize(
    "float_1, float_2",
    [(0.0, 0.0), (0.0, 1.0), (-1.0, 0.0)],
)
def test_clear_returns_invalid_empty_instance(float_1: float, float_2: float) -> None:
    """clear returns invalid and empty instance of ValueRange"""
    value_range = ValueRange.from_pair(float_1, float_2)
    assert value_range.is_valid()
    assert float_1 == value_range.lower()
    value_range.clear()
    assert not value_range.is_valid()
    assert value_range.lower() is None
    assert value_range.upper() is None


@pytest.mark.parametrize(
    "float_1, float_2, lower",
    [
        (0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (-1.0, 0.0, -1.0),
        (1.0, 0.0, 0.0),
        (0.0, -1.0, -1.0),
        (-1.0, 1.0, -1.0),
    ],
)
def test_lower_returns_lower_value(float_1: float, float_2: float, lower: float) -> None:
    """lower returns the lower value of ValueRange"""
    value_range = ValueRange.from_pair(float_1, float_2)
    assert min(float_1, float_2) == value_range.lower()
    assert lower == value_range.lower()


@pytest.mark.parametrize(
    "float_1, float_2, upper",
    [
        (0.0, 0.0, 0.0),
        (0.0, 1.0, 1.0),
        (-1.0, 0.0, 0.0),
        (1.0, 0.0, 1.0),
        (0.0, -1.0, 0.0),
        (-1.0, 1.0, 1.0),
    ],
)
def test_upper_returns_upper_value(float_1: float, float_2: float, upper: float) -> None:
    """upper returns the lower value of ValueRange"""
    value_range = ValueRange.from_pair(float_1, float_2)
    assert max(float_1, float_2) == value_range.upper()
    assert upper == value_range.upper()


@pytest.mark.parametrize(
    "float_1, float_2, difference",
    [
        (0.0, 0.0, 0.0),
        (0.0, 1.0, 1.0),
        (-1.0, 0.0, 1.0),
        (1.0, 0.0, 1.0),
        (0.0, -1.0, 1.0),
        (-1.0, 1.0, 2.0),
    ],
)
def test_diameter_returns_difference(float_1: float, float_2: float, difference: float) -> None:
    """diameter returns the difference of upper and lower"""
    value_range = ValueRange.from_pair(float_1, float_2)
    assert difference == value_range.diameter()


def test_diameter_on_invalid_returns_zero() -> None:
    """diameter on invalid instance returns 0"""
    value_range = ValueRange()
    assert not value_range.is_valid()
    assert 0.0 == value_range.diameter()


@pytest.mark.parametrize(
    "float_1, float_2, value",
    [
        (0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (-1.0, 0.0, 0.0),
        (1.0, 0.0, 0.1),
        (0.0, -1.0, -0.5),
        (-1.0, 1.0, -1),
    ],
)
def test_contains_returns_true(float_1: float, float_2: float, value: float) -> None:
    """contains returns True"""
    value_range = ValueRange.from_pair(float_1, float_2)
    assert value_range.contains(value)


@pytest.mark.parametrize(
    "float_1, float_2, value",
    [
        (0.0, 0.0, 1.0),
        (0.0, 1.0, 2.0),
        (-1.0, 0.0, 2.0),
        (1.0, 0.0, -1.0),
        (0.0, -1.0, 0.5),
        (-1.0, 1.0, -2),
    ],
)
def test_contains_returns_false(float_1: float, float_2: float, value: float) -> None:
    """contains returns False"""
    value_range = ValueRange.from_pair(float_1, float_2)
    assert not value_range.contains(value)


def test_contains_on_invalid_returns_false() -> None:
    """contains on invalid instance returns False"""
    value_range = ValueRange()
    assert not value_range.is_valid()
    assert not value_range.contains(1.0)


def test_extend_on_invalid_instance_instance_returns_valid() -> None:
    """extend on invalid instance returns valid instance with upper and lower"""
    value = 1.0
    value_range = ValueRange()
    assert not value_range.is_valid()
    value_range.extend(value)
    assert value_range.is_valid()
    assert value == value_range.lower()
    assert value == value_range.upper()


@pytest.mark.parametrize(
    "float_1, float_2, value",
    [
        (0.0, 0.0, 1.0),
        (0.0, 1.0, 2.0),
        (-1.0, 0.0, 2.0),
        (1.0, 0.0, -1.0),
        (0.0, -1.0, 0.5),
        (-1.0, 1.0, -2),
    ],
)
def test_extend_returns_extended_value_range(float_1: float, float_2: float, value: float) -> None:
    """extend returns a ValueRange with extended upper and/or lower"""
    value_range = ValueRange.from_pair(float_1, float_2)
    assert min(float_1, float_2) == value_range.lower()
    assert max(float_1, float_2) == value_range.upper()
    value_range.extend(value)
    assert min(float_1, float_2, value) == value_range.lower()
    assert max(float_1, float_2, value) == value_range.upper()


def test_interpolate_on_invalid_instance_raises_exception() -> None:
    """interpolate on invalid instance raises exception"""
    value_range = ValueRange()
    assert not value_range.is_valid()
    with pytest.raises(ValueError):
        value_range.interpolate(1.0)


@pytest.mark.parametrize(
    "float_1, float_2, value, expected",
    [
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 2.0, 1.0, 2.0),
        (-1.0, 0.0, 2.0, 1.0),
        (1.0, 0.0, -1.0, -1.0),
        (0.0, -1.0, 0.5, -0.5),
        (-1.0, 1.0, -2.0, -5.0),
    ],
)
def test_interpolate_on_valid_instance_returns_value(
    float_1: float, float_2: float, value: float, expected: float
) -> None:
    """interpolate returns interpolated value"""
    value_range = ValueRange.from_pair(float_1, float_2)
    assert expected == value_range.interpolate(value)


def test_relative_position_on_invalid_instance_raises_exception() -> None:
    """relative_position on invalid instance raises exception"""
    value_range = ValueRange()
    assert not value_range.is_valid()
    with pytest.raises(ValueError):
        value_range.relative_position(1.0)


@pytest.mark.parametrize(
    "float_1, float_2, value, expected",
    [
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 2.0, 1.0, 0.5),
        (-1.0, 0.0, 2.0, 1.0),
        (1.0, 0.0, -1.0, 0.0),
        (1.0, 1.0, 0.5, 0.0),
        (0.0, -2.0, -0.5, 0.75),
        (-1.0, 1.0, -0.5, 0.25),
    ],
)
def test_relative_position_on_valid_instance_returns_expected_value(
    float_1: float, float_2: float, value: float, expected: float
) -> None:
    """relative_position returns the relative position value"""
    value_range = ValueRange.from_pair(float_1, float_2)
    assert expected == value_range.relative_position(value)
