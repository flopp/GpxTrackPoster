.PHONY: lint test flake8 mypy spell check-format check-copyright bump-year update-readme format

lint: check-copyright flake8 mypy spell format-check

test:
	@python -m compileall create_poster.py gpxtrackposter
	@python -m pytest tests

flake8:
	@flake8 gpxtrackposter create_poster.py tests scripts

mypy:
	@mypy --ignore-missing-imports create_poster.py gpxtrackposter/*.py

spell:
	@codespell gpxtrackposter/*.py create_poster.py tests/*.py scripts/*.py

format-check:
	@black --check gpxtrackposter/*.py create_poster.py tests/*.py scripts/*.py

COPYRIGHT_FILES = README.md LICENSE create_poster.py gpxtrackposter/*.py tests/*.py scripts/*.py

check-copyright:
	@./scripts/check_copyright.py $(COPYRIGHT_FILES)

bump-year:
	@./scripts/bump_year.py $(COPYRIGHT_FILES)

update-readme:
	@./create_poster.py --help | ./scripts/update_readme.py README.md

format:
	@black gpxtrackposter/*.py create_poster.py tests/*.py scripts/*.py
