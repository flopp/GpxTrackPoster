# Copyright 2016-2022 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import locale


# day_of_week: 0-6 (0=Monday)
# If short is False return the full day name, otherwise return the shortest
# possible abbreviation (e.g. the first letter)
def localized_day_of_week_name(day_of_week: int, short: bool) -> str:
    assert 0 <= day_of_week <= 6

    locale_name = locale.getlocale()[0]

    name = locale.nl_langinfo(
        [
            locale.DAY_2,
            locale.DAY_3,
            locale.DAY_4,
            locale.DAY_5,
            locale.DAY_6,
            locale.DAY_7,
            locale.DAY_1,
        ][day_of_week]
    )
    if short:
        # special case for chinese: chinese weekday key number is the third
        if locale_name == "zh_CN":
            return name[2].upper()
        return name[0].upper()
    return name
