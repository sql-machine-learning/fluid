# -*- coding: utf-8 -*-
'''This module test fluid module version
'''
import fluid


def test_answer():
    ''' assert fluid module version'''
    assert fluid.__version__ == fluid.version.__version__
