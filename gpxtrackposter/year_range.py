# Copyright 2016-2018 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import re
from typing import Optional
from .track import Track


class YearRange:
    def __init__(self):
        self.from_year = None
        self.to_year = None

    def parse(self, s: str) -> bool:
        if s == 'all':
            self.from_year = None
            self.to_year = None
            return True
        m = re.match(r'^\d+$', s)
        if m:
            self.from_year = int(s)
            self.to_year = self.from_year
            return True
        m = re.match(r'^(\d+)-(\d+)$', s)
        if m:
            y1, y2 = int(m.group(1)), int(m.group(2))
            if y1 <= y2:
                self.from_year = y1
                self.to_year = y2
                return True
        return False

    def add(self, t: Track):
        if self.from_year is None:
            self.from_year = t.year
            self.to_year = t.year
        elif t.year < self.from_year:
            self.from_year = t.year
        elif t.year > self.to_year:
            self.to_year = t.year

    def contains(self, t: Track) -> bool:
        if self.from_year is None:
            return True
        return self.from_year <= t.year <= self.to_year

    def count(self) -> Optional[int]:
        if self.from_year is None:
            return None
        return 1 + self.to_year - self.from_year
