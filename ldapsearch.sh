#!/bin/bash
LDAPTLS_REQCERT=never ldapsearch -D 'AD\Administrator' -w 'P@ssw0rd' -H 'ldap://10.5.0.2' -b DC=ad,DC=zam,DC=haus -ZZ "$@"