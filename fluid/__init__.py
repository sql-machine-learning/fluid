# -*- coding: utf-8 -*-
'''This module expose Fluid API for users to write Fluid program
'''

from . import pyfunc
from .pyfunc import * # noqa
from . import version
from .version import __version__ # noqa

__all__ = pyfunc.__all__ + version.__all__
