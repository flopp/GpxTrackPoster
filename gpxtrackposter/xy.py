"""Represent x,y values with properly overloaded operations."""
# Copyright 2016-2023 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from math import isclose
from typing import Optional, Tuple, Union


class XY:
    """Represent x,y values with properly overloaded operations."""

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x: Union[int, float] = x
        self.y: Union[int, float] = y

    def __mul__(self, factor: Union[float, "XY"]) -> "XY":
        if isinstance(factor, XY):
            return XY(self.x * factor.x, self.y * factor.y)
        return XY(self.x * factor, self.y * factor)

    def __rmul__(self, factor: Union[float, "XY"]) -> "XY":
        if isinstance(factor, XY):
            return XY(self.x * factor.x, self.y * factor.y)
        return XY(self.x * factor, self.y * factor)

    def __truediv__(self, divisor: Union[float, "XY"]) -> "XY":
        if isinstance(divisor, XY):
            return XY(self.x / divisor.x, self.y / divisor.y)
        return XY(self.x / divisor, self.y / divisor)

    def __add__(self, other: Union[float, "XY"]) -> "XY":
        if isinstance(other, XY):
            return XY(self.x + other.x, self.y + other.y)
        return XY(self.x + other, self.y + other)

    def __radd__(self, other: Union[float, "XY"]) -> "XY":
        return self.__add__(other)

    def __sub__(self, other: Union[float, "XY"]) -> "XY":
        if isinstance(other, XY):
            return XY(self.x - other.x, self.y - other.y)
        return XY(self.x - other, self.y - other)

    def __repr__(self) -> str:
        return f"XY: {self.x}/{self.y}"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, XY) and isclose(self.x, other.x) and isclose(self.y, other.y)

    def tuple(self) -> Tuple[float, float]:
        """
        Return a tuple with the x and y values

        return: tuple with x and y values
        """
        return self.x, self.y

    def to_int(self) -> "XY":
        """
        Return an XY object with integer values

        return: XY object with integer x and y values
        """
        return XY(int(self.x), int(self.y))

    def round(self, n: Optional[int] = None) -> "XY":
        """
        Return an XY object with rounded values

        return: XY object with rounded x and y values
        """
        return XY(round(self.x, n), round(self.y, n))

    def get_max(self) -> Union[int, float]:
        """
        Return the maximum of the x and y value

        return: maximum value
        """
        return max([self.x, self.y])

    def get_min(self) -> Union[int, float]:
        """
        Return the minimum of the x and y value

        return: minimum value
        """
        return min([self.x, self.y])

    def scale_to_max_value(self, max_value: float) -> "XY":
        """
        Scale the x and y values to given maximum value

        max_value: maximum value to scale x and y values to
        return: XY object with scaled y and y values
        """
        if self.x > self.y:
            x = max_value
            y = x / self.x * self.y
        else:
            y = max_value
            x = y / self.y * self.x
        return XY(x, y)
