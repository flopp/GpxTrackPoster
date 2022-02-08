"""
Several tests for QuantityRange
"""
# Copyright 2021-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import pytest
from pint.quantity import Quantity  # type: ignore

from gpxtrackposter.quantity_range import QuantityRange


def test_init_returns_invalid_instance() -> None:
    """QuantityRange object is initialised with None values, thus invalid"""
    quantity_range = QuantityRange()
    assert not quantity_range.is_valid()


def test_from_pair_returns_instance() -> None:
    """from_pair returns instance of QuantityRange"""
    quantity_range = QuantityRange.from_pair(Quantity(0.0), Quantity(0.0))
    assert quantity_range.is_valid()
    assert isinstance(quantity_range, QuantityRange)


@pytest.mark.parametrize(
    "float_1, float_2",
    [(0.0, 0.0), (0.0, 1.0), (-1.0, 0.0)],
)
def test_clear_returns_invalid_empty_instance(float_1: float, float_2: float) -> None:
    """clear returns invalid and empty instance of QuantityRange"""
    expected_value = Quantity(float_1)
    quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
    assert quantity_range.is_valid()
    assert expected_value == quantity_range.lower()
    quantity_range.clear()
    assert not quantity_range.is_valid()
    assert quantity_range.lower() is None
    assert quantity_range.upper() is None


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
    """lower returns a Quantity instance of the lower value"""
    quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
    assert Quantity(min(float_1, float_2)) == quantity_range.lower()
    assert Quantity(lower) == quantity_range.lower()
    assert lower == quantity_range.lower()


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
    """upper returns a Quantity instance of the lower value"""
    quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
    assert Quantity(max(float_1, float_2)) == quantity_range.upper()
    assert Quantity(upper) == quantity_range.upper()
    assert upper == quantity_range.upper()


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
    """diameter returns a Quantity of the difference of upper and lower"""
    quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
    assert Quantity(difference) == quantity_range.diameter()
    assert difference == quantity_range.diameter()


def test_diameter_on_invalid_returns_zero() -> None:
    """diameter on invalid instance returns Quantity(0)"""
    quantity_range = QuantityRange()
    assert not quantity_range.is_valid()
    assert quantity_range.diameter() == Quantity(0.0)
    assert quantity_range.diameter() == 0.0


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
    quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
    assert quantity_range.contains(Quantity(value))


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
    quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
    assert not quantity_range.contains(Quantity(value))


def test_contains_on_invalid_returns_false() -> None:
    """contains on invalid instance returns False"""
    quantity_range = QuantityRange()
    assert not quantity_range.is_valid()
    assert not quantity_range.contains(Quantity(1.0))


def test_extend_on_invalid_instance_instance_returns_valid() -> None:
    """extend on invalid instance returns valid instance with upper and lower"""
    value = 1.0
    quantity_range = QuantityRange()
    assert not quantity_range.is_valid()
    quantity_range.extend(Quantity(value))
    assert quantity_range.is_valid()
    assert Quantity(value) == quantity_range.lower()
    assert Quantity(value) == quantity_range.upper()
    assert value == quantity_range.lower()
    assert value == quantity_range.upper()


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
def test_extend_returns_extended_quantity_range(float_1: float, float_2: float, value: float) -> None:
    """extend returns a QuantityRange with extended upper and/or lower"""
    quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
    assert Quantity(min(float_1, float_2)) == quantity_range.lower()
    assert Quantity(max(float_1, float_2)) == quantity_range.upper()
    quantity_range.extend(Quantity(value))
    assert Quantity(min(float_1, float_2, value)) == quantity_range.lower()
    assert Quantity(max(float_1, float_2, value)) == quantity_range.upper()
    assert min(float_1, float_2, value) == quantity_range.lower()
    assert max(float_1, float_2, value) == quantity_range.upper()


def test_interpolate_on_invalid_instance_raises_exception() -> None:
    """interpolate on invalid instance raises exception"""
    quantity_range = QuantityRange()
    assert not quantity_range.is_valid()
    with pytest.raises(ValueError):
        quantity_range.interpolate(1.0)


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
    """interpolate returns a Quantity with interpolated value"""
    quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
    assert Quantity(expected) == quantity_range.interpolate(value)
    assert expected == quantity_range.interpolate(value)


def test_relative_position_on_invalid_instance_raises_exception() -> None:
    """relative_position on invalid instance raises exception"""
    quantity_range = QuantityRange()
    assert not quantity_range.is_valid()
    with pytest.raises(ValueError):
        quantity_range.relative_position(Quantity(1.0))


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
    """relative_position returns a Quantity of the relative position value"""
    quantity_range = QuantityRange.from_pair(Quantity(float_1), Quantity(float_2))
    assert Quantity(expected) == quantity_range.relative_position(Quantity(value))
    assert expected == quantity_range.relative_position(Quantity(value))
