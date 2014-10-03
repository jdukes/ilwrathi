#!/usr/bin/env python
"""Ilwrath is a framwork for building web pen testing tools.

Ilwrath currently contains Sac. Sac is a base class that can be
extended to handle performing operations that have multiple
dependances. This was created to solve the problem of testing web
services with multiple dependances."""
from sys import version_info as _version_info

if _version_info.major == 2:
    from ._py2 import IdempotentAccessor

__all__ = ["IdempotentAccessor"]
