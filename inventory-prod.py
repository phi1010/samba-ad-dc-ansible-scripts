#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "icecream",
# ]
# ///
import subprocess
import json
import os, sys
import logging
import re
from typing import Any

from icecream import ic

HOSTS_PROD = [
    "ad001.srv.zam.haus",
    "ad002.srv.zam.haus",
]

log = logging.getLogger(__name__)


def run():
    print(json.dumps(get_inventory_object(HOSTS_PROD), indent=4))

def get_inventory_object(hosts) -> dict:
    return {
        "adcs": {
            "hosts": hosts,
            "vars": {
                "ansible_user": os.environ.get("USERNAME") or "ansible",
                #"ansible_password": "logmein",
                "ansible_ssh_port": 22,
                #"ansible_ssh_common_args": "-o StrictHostKeyChecking=no",
            }
        },
        "_meta": {
            "hostvars": {
                host: dict() for host in hosts
            }
        }
    }


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    ic.configureOutput(outputFunction=logging.debug)
    run()
