#!/usr/bin/env bash
set -euo pipefail
uv run ansible-inventory -i inventory.py "$*"
