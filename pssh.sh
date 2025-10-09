#!/usr/bin/env bash
set -euo pipefail
source env.sh
docker compose up -d
sshpass -p "$PASS" parallel-ssh -H ansible@localhost:2201 -H ansible@localhost:2202 -A -i "$*"
