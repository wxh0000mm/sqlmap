#!/usr/bin/env python

"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

import re

from lib.core.enums import HTTPHEADER
from lib.core.settings import WAF_ATTACK_VECTORS

__product__ = "NetScaler (Citrix Systems)"

def detect(get_page):
    page, headers, code = get_page()
    retval = re.search(r"\A(ns_af=|citrix_ns_id|NSC_)", headers.get(HTTPHEADER.SET_COOKIE, ""), re.I) is not None

    if not retval:
        for vector in WAF_ATTACK_VECTORS:
            page, headers, code = get_page(get=vector)
            retval = re.search(r"\Aclose", headers.get("Cneonction", "") or headers.get("nnCoection", ""), re.I) is not None
            if retval:
                break

    return retval