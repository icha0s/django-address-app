#!/usr/bin/env bash

set -e
set -x


pipenv run flake8 .

pipenv run black --check . --diff --target-version py38
pipenv run isort --recursive --check-only .