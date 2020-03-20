# -*- coding: utf-8 -*-
'''This module packages and distributes Fluid'''
import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'fluid'
DESCRIPTION = 'Tekton Workflow compiler.'
URL = 'https://github.com/wangkuiyi/fluid'
EMAIL = 'sqlflow@list.alibaba-inc.com'
AUTHOR = 'SQLFlow Dev'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = None

# What packages are required for this module to be executed?
REQUIRES = ['pyyaml']
TEST_REQUIRED = REQUIRES + [
    'pytest',
]

# What packages are optional?
EXTRAS = {}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier
# for that!

HERE = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
        LONG_DESCRIPTION = '\n' + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

# Load the package's version.py module as a dictionary.
ABOUT = {}
if not VERSION:
    with open(os.path.join(HERE, NAME, 'version.py')) as f:
        exec(f.read(), ABOUT)   # pylint: disable=exec-used
else:
    ABOUT['__version__'] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=ABOUT['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests', )),
    install_requires=REQUIRES,
    tests_require=TEST_REQUIRED,
    extras_require=EXTRAS,
    license='Apache License 2.0',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
