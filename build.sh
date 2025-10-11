#!/usr/bin/env bash
set -euo pipefail
. ./.env.sh
docker compose down
docker compose build
docker compose up -d
docker inspect -f \
  "ssh-keygen -f /home/phi1010/.ssh/known_hosts -R {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" \
  $(docker ps -aq) \
  | grep -P '\d+\.\d+\.\d+\.\d+' \
  | bash
./pssh.sh ""