#!/usr/bin/env python

# Copyright 2018 Florian Pigorsch & Contributors. All rights reserved.
#
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import os
import subprocess

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
readme_md_file_name = os.path.join(base_dir, 'README.md')
create_poster_py_file_name = os.path.join(base_dir, 'create_poster.py')

# read usage
usage = []
p = subprocess.Popen([create_poster_py_file_name, '--help'], stdout=subprocess.PIPE)
p.wait()
(stdout, stderr) = p.communicate()
usage = stdout.decode('utf-8')
assert usage.startswith('usage: create_poster.py')

# replace usage in README.md
lines = []
with open(readme_md_file_name, 'r') as f:
    lines = f.readlines()
with open(readme_md_file_name, 'w') as f:
    state = 0
    for line in lines:
        if state == 0:
            f.write(line)
            if line.startswith('## Usage'):
                state = 1
        elif state == 1:
            f.write(line)
            if line.startswith('```'):
                state = 2
                f.write(usage)
        elif state == 2:
            if line.startswith('```'):
                f.write(line)
                state = 3
        else:
            f.write(line)

# replace usage in create_poster.py's header
lines = []
with open(create_poster_py_file_name, 'r') as f:
    lines = f.readlines()
with open(create_poster_py_file_name, 'w') as f:
    state = 0
    for line in lines:
        if state == 0:
            if line.startswith('usage: create_poster.py'):
                f.write(usage)
                state = 1
            else:
                f.write(line)
        elif state == 1:
            if line.startswith('"""'):
                state = 2
                f.write(line)
        else:
            f.write(line)
