.PHONY: lint test pycodestyle mypy spell check-format check-copyright bump-year update-readme format

lint: check-copyright pycodestyle mypy spell format-check

test:
	@python -m compileall gpxtrackposter
	@python -m pytest tests

pycodestyle:
	@pycodestyle --max-line-length=120 gpxtrackposter tests scripts

mypy:
	@mypy --ignore-missing-imports gpxtrackposter/*.py

spell:
	@codespell gpxtrackposter/*.py tests/*.py scripts/*.py

format-check:
	@black --check gpxtrackposter/*.py tests/*.py scripts/*.py

COPYRIGHT_FILES = README.md LICENSE gpxtrackposter/*.py tests/*.py scripts/*.py

check-copyright:
	@./scripts/check_copyright.py $(COPYRIGHT_FILES)

bump-year:
	@./scripts/bump_year.py $(COPYRIGHT_FILES)

update-readme:
	@./gpxtrackposter/cli.py --help | ./scripts/update_readme.py README.md

format:
	@black gpxtrackposter/*.py tests/*.py scripts/*.py
