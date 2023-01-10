"""Represent a range of numerical values"""
# Copyright 2016-2023 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import typing


class ValueRange:
    """Represent a range of numerical values.

    Attributes:
        _lower: Lower bound of range.
        _upper: Upper bound of range.

    Methods:
        from_pair: Return a new ValueRange object from a pair of floats.
        is_valid: Return True if lower bound is set, else False.
        lower: Return lower bound.
        upper: Return upper bound.
        diameter: Return difference between upper and lower bounds if valid, else 0.
        contains: Returns True if the range contains value.
        extend: Adjust the range to include value.
        interpolate: Return interpolated value.
        relative_position: Return relative position of value with respect to lower and upper of ValueRange
    """

    def __init__(self) -> None:
        self._lower: typing.Optional[float] = None
        self._upper: typing.Optional[float] = None

    @classmethod
    def from_pair(cls, value1: float, value2: float) -> "ValueRange":
        r = cls()
        r.extend(value1)
        r.extend(value2)
        return r

    def clear(self) -> None:
        self._lower = None
        self._upper = None

    def is_valid(self) -> bool:
        return self._lower is not None

    def lower(self) -> typing.Optional[float]:
        return self._lower

    def upper(self) -> typing.Optional[float]:
        return self._upper

    def diameter(self) -> float:
        if self.is_valid():
            assert self._upper is not None
            assert self._lower is not None
            return self._upper - self._lower
        return 0

    def contains(self, value: float) -> bool:
        if not self.is_valid():
            return False

        assert self._upper is not None
        assert self._lower is not None
        return self._lower <= value <= self._upper

    def extend(self, value: float) -> None:
        if not self.is_valid():
            self._lower = value
            self._upper = value
        else:
            assert self._upper is not None
            assert self._lower is not None
            self._lower = min(self._lower, value)
            self._upper = max(self._upper, value)

    def interpolate(self, relative: float) -> float:
        if not self.is_valid():
            raise ValueError("Cannot interpolate invalid ValueRange")
        assert self._lower is not None
        assert self._upper is not None
        return self._lower + relative * (self._upper - self._lower)

    def relative_position(self, value: float) -> float:
        if not self.is_valid():
            raise ValueError("Cannot get relative_position for invalid ValueRange")
        assert self._lower is not None
        assert self._upper is not None
        if value <= self._lower:
            return 0.0
        if value >= self._upper:
            return 1.0
        diff = self._upper - self._lower
        if diff == 0:
            return 0.0
        return (value - self._lower) / diff
