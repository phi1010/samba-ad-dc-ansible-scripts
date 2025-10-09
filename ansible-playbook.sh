#!/usr/bin/env bash
set -euxo pipefail
ANSIBLE_STDOUT_CALLBACK=debug uv run ansible-playbook -i inventory.py "$@"