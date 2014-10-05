#/usr/bin/env python
from sys import version_info as _version_info

if _version_info.major == 2:
    from test_ilwrathi__py2_iac import TestIdempotentAccessor

#add doctests??
