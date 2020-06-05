#!/usr/bin/env bash

set -e

pipenv run autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place . --exclude=__init__.py
pipenv run black . --target-version py38
pipenv run isort --recursive .