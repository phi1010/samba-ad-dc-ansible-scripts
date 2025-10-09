#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import sys

DOCUMENTATION = r'''
'''

EXAMPLES = r'''
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
import traceback
import socket
import json
import pprint

try:
    import dns.resolver
except ImportError:
    IMPORT_ERROR = traceback.format_exc()
else:
    IMPORT_ERROR = None


def run_module():
    module_args = dict(
        adc_list=dict(type='list', required=True),
        domain=dict(type='str', required=True),
    )
    result = dict(
        changed=False,
        locals="",
        msg="",
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    if IMPORT_ERROR is not None:
        module.fail_json(msg=IMPORT_ERROR, **result)

    try:
        adcs = module.params['adc_list']
        domain = module.params['domain']

        def getaddrinfos(family, adcs):
            return {
                host:
                    [addrinfo[4][0] for addrinfo in socket.getaddrinfo(
                        host,
                        None,
                        family,
                        socket.SOCK_STREAM,
                    )]
                for host in adcs
            }

        ipv4s = getaddrinfos(socket.AddressFamily.AF_INET, adcs)
        # ipv6s = getaddrinfos(socket.AddressFamily.AF_INET6, adcs)
        allipv4s = set(sum(ipv4s.values(), []))

        def get_ips(domain, record_type, resolver_ip=None):
            resolver = dns.resolver.Resolver()
            if resolver_ip is not None:
                resolver.nameservers = [resolver_ip]
            answers = resolver.resolve(domain, record_type)
            return [answer.to_text() for answer in answers]

        for resolver in allipv4s:

            def check_all_adcs_in_srv_record(srv_domain):
                ipset = set()
                answers = get_ips(srv_domain, "SRV", resolver)

                for srv_entry in answers:
                    hostname = srv_entry.split()[3]
                    try:
                        ip, = get_ips(hostname, "A", resolver)
                    except:
                        module.fail_json(error=f"Could not resolve hostname {hostname} from SRV record {srv_entry} for {srv_domain} from resolver {resolver}", **result)
                    else:
                        ipset.add(ip)
                assert ipset == allipv4s, f"IPs {ipset} for {srv_domain} from resolver {resolver} do not match ADC IPs {allipv4s}"

            def check_all_adcs_in_a_record(a_domain):
                ipset = set()
                answers = get_ips(a_domain, "A", resolver)
                result["msg"] = pprint.pformat(answers, indent=4)
                for a_entry in answers:
                    ipset.add(a_entry)
                assert ipset == allipv4s, f"IPs {ipset} for {a_domain} from resolver {resolver} do not match ADC IPs {allipv4s}"

            check_all_adcs_in_srv_record("_ldap._tcp." + domain)
            check_all_adcs_in_srv_record("_kerberos._tcp." + domain)
            check_all_adcs_in_srv_record("_gc._tcp." + domain)
            check_all_adcs_in_a_record(domain)

    except Exception:
        # result["locals"] = pprint.pformat(locals(), indent=4)
        module.fail_json(error=traceback.format_exc(), **result)
    else:
        # result["locals"] = pprint.pformat(locals(), indent=4)
        pass

    if module.check_mode:
        module.exit_json(**result)

    # No change ops for this module, just a test
    result['changed'] = False
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
