#!/usr/bin/env python3

import setuptools
import os


def _read_reqs(relpath):
    fullpath = os.path.join(os.path.dirname(__file__), relpath)
    with open(fullpath) as f:
        return [s.strip() for s in f.readlines()
                if (s.strip() and not s.startswith("#"))]


setuptools.setup(
    name='gpxtrackposter',
    version='0.1',
    install_requires=_read_reqs("requirements.txt"),
    tests_require=_read_reqs("requirements-dev.txt"),
    data_files=[('.', ['requirements.txt', 'requirements-dev.txt'])],
    packages=setuptools.find_packages(),
)
