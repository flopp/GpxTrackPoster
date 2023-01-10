PROJECT = gpxtrackposter
SRC_CORE = gpxtrackposter
SRC_SCRIPTS = scripts
SRC_TEST = tests
SRC_COMPLETE = $(SRC_CORE) $(SRC_TEST) $(SRC_SCRIPTS)
COPYRIGHT_FILES = $(SRC_CORE) $(SRC_TEST) $(SRC_SCRIPTS) README.md LICENSE
PYTHON=python3
PIP=$(PYTHON) -m pip

help: ## Print help for each target
	$(info Makefile low-level Python API.)
	$(info =============================)
	$(info )
	$(info Available commands:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'

clean: ## Cleanup
	@rm -f  ./*.pyc
	@rm -rf ./__pycache__
	@rm -f  $(SRC_CORE)/*.pyc
	@rm -rf $(SRC_CORE)/__pycache__
	@rm -f  $(SRC_TEST)/*.pyc
	@rm -rf $(SRC_TEST)/__pycache__
	@rm -f  $(SRC_EXAMPLES)/*.pyc
	@rm -rf $(SRC_EXAMPLES)/__pycache__
	@rm -rf ./.coverage
	@rm -rf ./coverage.xml
	@rm -rf ./.pytest_cache
	@rm -rf ./.mypy_cache
	@rm -rf ./site
	@rm -rf ./reports

.PHONY: setup
setup: ## Setup virtual environment
	$(PYTHON) -m venv .env
	.env/bin/pip install --upgrade pip wheel
	.env/bin/pip install --upgrade -r requirements.txt
	.env/bin/pip install --upgrade -r requirements-dev.txt

.PHONY: install
install: setup ## install package
	.env/bin/pip install .

.PHONY: check-copyright
check-copyright: ## check copyright
	.env/bin/python scripts/check_copyright.py $(COPYRIGHT_FILES)

.PHONY: bump-year
bump-year: ## bump year to current
	.env/bin/python scripts/bump_year.py $(COPYRIGHT_FILES)

.PHONY: update-readme
update-readme: ## update readme to output of 'gpxtrackposter --help'
	PYTHON_PATH=. .env/bin/python gpxtrackposter/cli.py --help | .env/bin/python scripts/update_readme.py README.md

.PHONY: format
format: ## Format the code
	.env/bin/isort \
		setup.py $(SRC_COMPLETE)
	.env/bin/autopep8 \
		-i -r \
		setup.py $(SRC_COMPLETE)
	.env/bin/black \
		--line-length 120 \
		setup.py $(SRC_COMPLETE)

.PHONY: lint
lint: ## Lint the code
	.env/bin/pycodestyle \
	--max-line-length=120 \
		setup.py $(SRC_COMPLETE)
	.env/bin/isort \
		setup.py $(SRC_COMPLETE) \
		--check --diff
	.env/bin/black \
	    --line-length 120 \
	    --check \
	    --diff \
	    setup.py $(SRC_COMPLETE)
	.env/bin/pyflakes \
		setup.py $(SRC_COMPLETE)
	.env/bin/flake8 \
		setup.py $(SRC_COMPLETE)
	.env/bin/pylint \
		setup.py $(SRC_COMPLETE)
	.env/bin/mypy \
		setup.py $(SRC_COMPLETE)
	.env/bin/codespell \
	    README.md setup.py gpxtrackposter/*.py tests/*.py scripts/*.py

.PHONY: test
test: ## Test the code
	.env/bin/pytest tests

.PHONY: coverage
coverage: ## Generate coverage report for the code
	.env/bin/pytest --cov=gpxtrackposter --cov-branch --cov-report=term --cov-report=html tests -m "not full_run"

.PHONY: coverage_with_full_run
coverage_with_full_run: ## Generate coverage report for the code including tests marked as 'full_run'
	.env/bin/pytest --cov=gpxtrackposter --cov-branch --cov-report=term --cov-report=html tests

.PHONY: extract-messages
extract-messages: ## extract messages from pot files
	xgettext --keyword="translate" -d gpxposter -o locale/gpxposter.pot gpxtrackposter/*.py
	msgmerge --update locale/de_DE/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/fi_FI/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/fr_FR/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/ru_RU/LC_MESSAGES/gpxposter.po locale/gpxposter.pot
	msgmerge --update locale/zh_CN/LC_MESSAGES/gpxposter.po locale/gpxposter.pot

.PHONY: compile-messages
compile-messages: ## compile messages
	msgfmt -o locale/de_DE/LC_MESSAGES/gpxposter.mo locale/de_DE/LC_MESSAGES/gpxposter
	msgfmt -o locale/fi_FI/LC_MESSAGES/gpxposter.mo locale/fi_FI/LC_MESSAGES/gpxposter
	msgfmt -o locale/fr_FR/LC_MESSAGES/gpxposter.mo locale/fr_FR/LC_MESSAGES/gpxposter
	msgfmt -o locale/ru_RU/LC_MESSAGES/gpxposter.mo locale/ru_RU/LC_MESSAGES/gpxposter
	msgfmt -o locale/zh_CN/LC_MESSAGES/gpxposter.mo locale/zh_CN/LC_MESSAGES/gpxposter
