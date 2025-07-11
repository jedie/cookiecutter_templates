SHELL := /bin/bash
export PATH := .venv/bin:$(PATH)

all: help

.PHONY: help
help:  ## List all commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -_]+:.*?## / {printf "\033[36m%-26s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install-base-req
install-base-req:  ## Install needed base packages via apt
	sudo apt install python3-pip python3-venv

.PHONY: install
install:  ## Install the project in a Python virtualenv
	python3 -m venv .venv
	.venv/bin/pip install -U pip
	.venv/bin/pip install -U uv
	.venv/bin/uv sync

.PHONY: update-requirements
update-requirements:  ## Update requirements
	python3 -m venv .venv
	.venv/bin/pip install -U pip
	.venv/bin/pip install -U uv
	.venv/bin/uv lock --upgrade
	.venv/bin/uv sync

.PHONY: lint
lint: ## Run code formatters and linter
	.venv/bin/darker --diff --check
	.venv/bin/flake8 .

.PHONY: fix-code-style
fix-code-style: ## Fix code formatting
	.venv/bin/darker
	.venv/bin/flake8 .

.PHONY: nox
nox:  ## Run tests via nox with all environments
	.venv/bin/nox

.PHONY: test
test: ## Run tests
	.venv/bin/python3 -m unittest --verbose --locals

.PHONY: coverage
coverage:  ## Run tests with coverage
	.venv/bin/coverage run
	.venv/bin/coverage combine --append
	.venv/bin/coverage report
	.venv/bin/coverage xml
	.venv/bin/coverage json

.PHONY: update-test-snapshot-files
update-test-snapshot-files:   ## Update all snapshot files (by remove and recreate all snapshot files)
	find . -type f -name '*.snapshot.*' -delete
	RAISE_SNAPSHOT_ERRORS=0 .venv/bin/python3 -m unittest

.PHONY: mypy
mypy:  ## Run mypy
	.venv/bin/mypy .

.PHONY: pip-audit
pip-audit:  ## Run https://github.com/pypa/pip-audit
	.venv/bin/uv export --no-header --frozen --no-editable --no-emit-project -o /tmp/temp_requirements.txt
	.venv/bin/pip-audit --strict --require-hashes -r /tmp/temp_requirements.txt

.PHONY: publish
publish:  ## Release new version to PyPi
	.venv/bin/pip install -e .
	.venv/bin/python3 {{ cookiecutter.package_name }}_tests/publish.py

.PHONY: clean
clean: ## Remove created files from the test project
	git clean -dfX {{ cookiecutter.package_name }}_tests/