#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "docopt",
#     "dynaconf",
#     "icecream",
#     "rich",
# ]
# ///
"""
RDP script to connect to a remote Windows host via Remote Desktop Protocol (RDP).

Usage:
    rdp.py [--host=<host>] [--user=<user>] [--password=<password>] [--port=<port>] [--domain=<domain>] [--driver=<driver>]
    rdp.py (-h | --help)

Options:
    --host=<host>           The hostname or IP address of the remote Windows host [default: localhost].
    --user=<user>           The username for RDP connection. Is determined from the domain if not provided.
    --password=<password>   The password for RDP connection. Is determined from the domain if not provided.
    --port=<port>           The port for RDP connection [default: 3389].
    --domain=<domain>       The domain for RDP connection (e.g. 'AD', or '.') [default: .].
    --driver=<driver>       The RDP client to use (e.g., 'xfreerdp3', 'remmina') [default: remmina].
    -h --help               Show this help message.
"""
import subprocess
import json
import os, sys
import logging
import re
import shlex
from dynaconf import Dynaconf
from docopt import docopt
from icecream import ic
from urllib.parse import quote

log = logging.getLogger(__name__)

settings = Dynaconf(
    settings_files=[f'{__file__}.toml'],
)

def main(args):
    host = args.get('--host', '')
    user = args.get('--user', '')
    password = args.get('--password', '')
    port = args.get('--port', '')
    domain = args.get('--domain', '')
    driver = args.get('--driver', '')

    if not host:
        log.fatal("Error: --host is required")
        sys.exit(1)

    if not user:
        user = settings.default_credentials.get(domain, dict()).get('username', '')
    if not password:
        password = settings.default_credentials.get(domain, dict()).get('password', '')
    if not domain:
        domain = "."
    if not port:
        port = "3389"
    if not user:
        log.fatal(f"Error: --user is required if domain is not in {list(settings.default_credentials.keys())}")
        sys.exit(1)
    if not password:
        log.fatal(f"Error: --password is required if domain is not in {list(settings.default_credentials.keys())}")
        sys.exit(1)
    ic(host, user, password, port, domain, driver)
    if driver == 'remmina':
        rdp_command = [
            driver,
            f"rdp://{
            quote(user) + (
                ":" + quote(password)
                if password else
                ""
            ) + '@'
            if user else 
            ''}{host}:{port}",
        ]
    elif driver == 'xfreerdp3':
        rdp_command = [
            driver,
            f"/v:{host}:{port}",
            f"/u:{user}",
            *([f"/d:{domain}"] if domain and domain != '.' else []),
            f"/p:{password}",
            "+dynamic-resolution"
    ]
    else:
        print("Error: --driver must be either 'xfreerdp3' or 'remmina'")
        sys.exit(1)

    log.info(f"Executing command: {shlex.join(rdp_command)}")

    try:
        subprocess.run(rdp_command, check=True)
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to connect via RDP: {e}")
        sys.exit(1)


if __name__ == "__main__":
    ic.configureOutput(outputFunction=log.debug)
    logging.basicConfig(level=logging.DEBUG)
    arguments = docopt(__doc__)
    ic(arguments)
    main(arguments)
