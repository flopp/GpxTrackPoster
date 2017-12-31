# Copyright 2016-2017 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.


class ValueRange:
    def __init__(self):
        self._lower = None
        self._upper = None

    def is_valid(self):
        return self._lower is not None

    def lower(self):
        return self._lower

    def upper(self):
        return self._upper

    def diameter(self):
        if self.is_valid():
            return self.upper() - self.lower()
        return 0

    def extend(self, value):
        if not self.is_valid():
            self._lower = value
            self._upper = value
        else:
            self._lower = min(self._lower, value)
            self._upper = max(self._upper, value)
