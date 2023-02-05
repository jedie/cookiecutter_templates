SHELL := /bin/bash
MAX_LINE_LENGTH := 119

help:  ## List all commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9 -_]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install the project in a Python virtualenv
	python3 -m venv .venv
	.venv/bin/pip install -U pipenv
	.venv/bin/pipenv install --dev

update-requirements:  ## Update requirements
	.venv/bin/pipenv update --dev

lint:  ## Run code formatters and linter
	.venv/bin/isort --check-only .
	.venv/bin/flake8 .

fix-code-style:  ## Fix code formatting
	.venv/bin/black --verbose --safe --line-length=${MAX_LINE_LENGTH} --skip-string-normalization .
	.venv/bin/isort .

tox-listenvs:  ## List all tox test environments
	.venv/bin/tox --listenvs

tox:  ## Run tests via tox with all environments
	.venv/bin/tox

test: ## Run tests
	.venv/bin/python -m unittest --verbose --locals