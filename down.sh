#!/bin/bash
set -euxo pipefail
docker-compose down -v
sudo rm -rf ./dockur/host1/storage