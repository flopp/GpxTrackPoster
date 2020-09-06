#!/usr/bin/env python3

import os

import setuptools


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
    data_files=[
        ('.', ['requirements.txt', 'requirements-dev.txt']),
        ('share/locale/de_DE/LC_MESSAGES', ['locale/de_DE/LC_MESSAGES/gpxposter.mo']),
        ('share/locale/fi_FI/LC_MESSAGES', ['locale/fi_FI/LC_MESSAGES/gpxposter.mo']),
        ('share/locale/fr_FR/LC_MESSAGES', ['locale/fr_FR/LC_MESSAGES/gpxposter.mo']),
        ('share/locale/ru_RU/LC_MESSAGES', ['locale/ru_RU/LC_MESSAGES/gpxposter.mo']),
        ('share/locale/zh_CN/LC_MESSAGES', ['locale/zh_CN/LC_MESSAGES/gpxposter.mo']),
        ],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'create_poster = gpxtrackposter.cli:main',
        ],
    },
)
data_files=[
        ('share/locale/ar/LC_MESSAGES', ['locale/ar/LC_MESSAGES/hatta.mo']),
        ('share/locale/cs/LC_MESSAGES', ['locale/cs/LC_MESSAGES/hatta.mo']),
        ('share/locale/da/LC_MESSAGES', ['locale/da/LC_MESSAGES/hatta.mo']),
        ('share/locale/de/LC_MESSAGES', ['locale/de/LC_MESSAGES/hatta.mo']),
        ('share/locale/el/LC_MESSAGES', ['locale/el/LC_MESSAGES/hatta.mo']),
        ('share/locale/es/LC_MESSAGES', ['locale/es/LC_MESSAGES/hatta.mo']),
        ('share/locale/et/LC_MESSAGES', ['locale/et/LC_MESSAGES/hatta.mo']),
        ('share/locale/fi/LC_MESSAGES', ['locale/fi/LC_MESSAGES/hatta.mo']),
        ('share/locale/fr/LC_MESSAGES', ['locale/fr/LC_MESSAGES/hatta.mo']),
        ('share/locale/hu/LC_MESSAGES', ['locale/hu/LC_MESSAGES/hatta.mo']),
        ('share/locale/ja/LC_MESSAGES', ['locale/ja/LC_MESSAGES/hatta.mo']),
        ('share/locale/lt/LC_MESSAGES', ['locale/lt/LC_MESSAGES/hatta.mo']),
        ('share/locale/pl/LC_MESSAGES', ['locale/pl/LC_MESSAGES/hatta.mo']),
        ('share/locale/ru/LC_MESSAGES', ['locale/ru/LC_MESSAGES/hatta.mo']),
        ('share/locale/sv/LC_MESSAGES', ['locale/sv/LC_MESSAGES/hatta.mo']),
        ('share/locale/vi/LC_MESSAGES', ['locale/vi/LC_MESSAGES/hatta.mo']),
        ('share/doc/hatta/examples', [
            'examples/hatta.fcgi',
            'examples/hatta.gzip.fcgi',
            'examples/hatta.wsgi',
            'examples/extend_parser.py'
        ]),
    ],