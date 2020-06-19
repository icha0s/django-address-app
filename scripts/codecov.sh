#!/usr/bin/env bash

set -e

bash <(curl -s https://codecov.io/bash) ${@}
