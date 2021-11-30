#!/usr/bin/env python

# Copyright 2018-2021 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import sys

usage = sys.stdin.read()
if not usage.startswith("usage: create_poster"):
    raise RuntimeError("Bad usage info from stdin")

readme_md_file_name = sys.argv[1]
if not readme_md_file_name.endswith("README.md"):
    raise RuntimeError(f"Bad README.md file: {readme_md_file_name}")

# replace usage in README.md
with open(readme_md_file_name, "r", encoding="utf8") as f:
    lines = f.readlines()

with open(readme_md_file_name, "w", encoding="utf8") as f:
    STATE = 0
    for line in lines:
        if STATE == 0:
            if line.startswith("usage: create_poster"):
                f.write(usage)
                STATE = 1
            else:
                f.write(line)
        elif STATE == 1:
            if line.startswith("```"):
                f.write(line)
                STATE = 2
        else:
            f.write(line)
