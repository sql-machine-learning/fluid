# -*- coding: utf-8 -*-
'''This module defines Kubernetes related utilities.'''

import re


def safe_name(name):
    '''Replace "_", ".", "\", "/" in name by "-"'''
    _sub = re.sub(r"_|\.|\\|/", "-", name)
    return _sub.strip("-")
