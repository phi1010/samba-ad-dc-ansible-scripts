#!/usr/bin/env bash
set -euxo pipefail
./ansible.sh -m ansible.builtin.gather_facts #-a "filter=ansible_distribution*"
