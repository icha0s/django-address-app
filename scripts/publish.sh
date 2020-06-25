#!/usr/bin/env bash

set -e
set -x

pipenv run twine upload dist/* ${@}