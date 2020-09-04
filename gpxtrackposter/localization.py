# Copyright 2016-2020 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import locale


# month: 1-12 (1=January)
def localized_month_name(month: int) -> str:
    assert 1 <= month <= 12

    # locale_name = locale.getlocale()[0]

    # special case for russian
    # if locale_name == "ru_RU":
    #    return ...

    # default
    return locale.nl_langinfo(
        [
            locale.MON_1,
            locale.MON_2,
            locale.MON_3,
            locale.MON_4,
            locale.MON_5,
            locale.MON_6,
            locale.MON_7,
            locale.MON_8,
            locale.MON_9,
            locale.MON_10,
            locale.MON_11,
            locale.MON_12,
        ][month - 1]
    )


# day_of_week: 0-6 (0=Monday)
# If short is False return the full day name, otherwise return the shortest
# possible abbreviation (e.g. the first letter)
def localized_day_of_week_name(day_of_week: int, short: bool) -> str:
    assert 1 <= day_of_week <= 7

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
