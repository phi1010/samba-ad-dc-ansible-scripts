#!/usr/bin/env bash
set -euo pipefail
source env.sh
docker compose down
docker compose build
docker compose up -d
docker inspect -f \
  "ssh-keygen -f /home/phi1010/.ssh/known_hosts -R {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" \
  $(docker ps -aq) \
  | grep -P '\d+\.\d+\.\d+\.\d+' \
  | bash
sshpass -p "$PASS" parallel-ssh -H ansible@localhost:2201 -H ansible@localhost:2202 -A -i ""