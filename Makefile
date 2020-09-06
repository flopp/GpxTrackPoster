.PHONY: check-copyright bump-year update-readme format extract-messages


COPYRIGHT_FILES = README.md LICENSE gpxtrackposter/*.py tests/*.py scripts/*.py

setup:
	python3 -m venv .env
	.env/bin/pip install --upgrade pip
	.env/bin/pip install -r requirements.txt
	.env/bin/pip install -r requirements-dev.txt
	.env/bin/pip install .

check-copyright:
	.env/bin/python scripts/check_copyright.py $(COPYRIGHT_FILES)

bump-year:
	.env/bin/python scripts/bump_year.py $(COPYRIGHT_FILES)

update-readme:
	PYTHON_PATH=. .env/bin/python gpxtrackposter/cli.py --help | .env/bin/python scripts/update_readme.py README.md

format:
	.env/bin/black \
	    --line-length 120 \
		gpxtrackposter tests scripts

.PHONY: lint
lint:
	.env/bin/pylint \
	    gpxtrackposter tests scripts
	.env/bin/mypy \
	    gpxtrackposter tests scripts
	.env/bin/codespell  \
	    README.md gpxtrackposter/*.py tests/*.py scripts/*.py
	.env/bin/black \
	    --line-length 120 \
	    --check \
	    --diff \
	    gpxtrackposter tests scripts

extract-messages:
	xgettext --keyword="trans" -d gpxposter -o locale/gpxposter.pot gpxtrackposter/*.py
	msgmerge --update locale/de_DE/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/fi_FI/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/fr_FR/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/ru_RU/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/zh_CN/LC_MESSAGES/gpxposter.po locale/gpxposter.pot

compile-messages:
	msgfmt -o locale/de_DE/LC_MESSAGES/gpxposter.mo locale/de_DE/LC_MESSAGES/gpxposter
	msgfmt -o locale/fi_FI/LC_MESSAGES/gpxposter.mo locale/fi_FI/LC_MESSAGES/gpxposter
	msgfmt -o locale/fr_FR/LC_MESSAGES/gpxposter.mo locale/fr_FR/LC_MESSAGES/gpxposter
	msgfmt -o locale/ru_RU/LC_MESSAGES/gpxposter.mo locale/ru_RU/LC_MESSAGES/gpxposter
	msgfmt -o locale/zh_CN/LC_MESSAGES/gpxposter.mo locale/zh_CN/LC_MESSAGES/gpxposter
