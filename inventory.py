#!/usr/bin/env -S uv run --script
import subprocess
import json
import os, sys
import logging
import re
from typing import Any

from icecream import ic

log = logging.getLogger(__name__)


def run():
    hosts = query_hosts()
    hosts = sorted(hosts, key=lambda host: host[0], reverse=True)
    print(json.dumps(get_inventory_object(hosts), indent=4))


def query_hosts() -> list[Any]:
    containers = (
        subprocess.run(
            ["docker", "ps", "-aq"],
            capture_output=True,
            check=True
        ).stdout.split()
    )
    data = subprocess.run(
        [
            "docker", "inspect", "-f",
            r"{{.Name}}={{range .NetworkSettings.Networks}}{{.IPAddress}},{{end}}",
            *containers
        ],
        capture_output=True,
        check=True,
        encoding="utf-8"
    )
    # log.debug("\n%s", data.stdout)
    hosts = []
    for line in data.stdout.splitlines():
        host, ips = line.split("=", 1)
        ips = [x for x in ips.split(",") if x]
        ic(host, ips)
        hosts.append((host, ips))
    return hosts


def get_inventory_object(hosts: list[Any]) -> dict[
    str, dict[str, list[Any] | dict[str, str | int]] | dict[str, dict[Any, dict[Any, Any]]]]:
    return {
        "docker": {
            "hosts": [
                ips[0] for host, ips in hosts if ips and host.endswith("-ansible")
            ],
            "vars": {
                "become_ansible_user": "ansible",
                "become_ansible_password": "logmein",
                "ansible_user": "ansible",
                "ansible_password": "logmein",
                "ansible_ssh_port": 22,
                "ansible_ssh_common_args": "-o StrictHostKeyChecking=no",
            }
        },
        "_meta": {
            "hostvars": {
                ip: dict()
                for host, ips in hosts for ip in ips
            }
        }
    }


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    ic.configureOutput(outputFunction=logging.debug)
    run()
