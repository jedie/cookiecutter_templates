#!/bin/sh

set -ex

exec .venv/bin/python -m {{ cookiecutter.package_name }} "$@"

