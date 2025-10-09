#!/usr/bin/env bash
set -euxo pipefail
uv run ansible docker -i inventory.py "$@"