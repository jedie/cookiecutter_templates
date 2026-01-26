SHELL := /bin/bash

all: help

.PHONY: help
help:  ## List all commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -_]+:.*?## / {printf "\033[36m%-26s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install:  ## Install via "uv" (Used system installed "uv" tool, e.g.: "pipx install uv")
	uv sync

.PHONY: update-requirements
update-requirements:  ## Update requirements
	uv lock --upgrade
	uv sync
	$(make) pip-audit

.PHONY: lint
lint: ## Check/fix code style by run: "ruff check --fix"
	uv run ruff check --fix

.PHONY: nox
nox:  ## Run tests via nox with all environments
	uv run nox

.PHONY: test
test: ## Run tests
	uv run python3 -m unittest --verbose --locals

.PHONY: coverage
coverage:  ## Run tests with coverage
	uv run coverage run
	uv run coverage combine --append
	uv run coverage report
	uv run coverage xml
	uv run coverage json

.PHONY: update-test-snapshot-files
update-test-snapshot-files:   ## Update all snapshot files (by remove and recreate all snapshot files)
	find . -type f -name '*.snapshot.*' -delete
	RAISE_SNAPSHOT_ERRORS=0 uv run python3 -m unittest

.PHONY: mypy
mypy:  ## Run mypy
	uv run mypy .

.PHONY: pip-audit
pip-audit:  ## Run https://github.com/pypa/pip-audit
	uv export --no-header --locked --no-emit-project > /tmp/temp_requirements.txt
	uv run pip-audit --skip-editable --strict --require-hashes --disable-pip -r /tmp/temp_requirements.txt


.PHONY: publish
publish:  ## Release new version to PyPi
	uv run pip install -e .
	uv run python3 your_cool_package_tests/publish.py

.PHONY: clean
clean: ## Remove created files from the test project
	git clean -dfX your_cool_package_tests/