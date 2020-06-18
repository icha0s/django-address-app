#!/usr/bin/env bash

set -e
set -x

pipenv run pytest --cov=django_address --cov=tests --cov-report=xml --cov-config=setup.cfg ${@}