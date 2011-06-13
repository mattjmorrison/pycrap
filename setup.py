# Copyright (C) 2011 Matthew J. Morrison
# E-mail: mattjmorrison AT mattjmorrison DOT com

from setuptools import setup

import os

VERSION = '0.0.1'
NAME = "pycrap"
AUTHOR = 'Matthew J. Morrison'
AUTHOR_EMAIL = 'mattjmorrison@mattjmorrison.com'
URL = 'http://www.pycrap.com'
DESCRIPTION = "A Python code Change Risk Analyzer and Predictor (a.k.a. CRAP)"
readme = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(readme).read()

PACKAGES = ('pycrap', )
MODULES = ('cc', 'pygenie', )
REQUIREMENTS = ('coverage', 'import_file', ) #'pygenie'
TEST_REQUIREMENTS = ('mock', )
TEST_SUITE = 'tests.SUITE'
ENTRY_POINTS = {'console_scripts': [
    'pycrap = pycrap:run',
    'pygenie = pygenie:main'
]}
CLASSIFIERS = (
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
#    "Programming Language :: Python :: 2.5", #TODO ?
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
#    "Programming Language :: Python :: 3.1 #TODO Depends on cc.py
#    "Programming Language :: Python :: 3.2 #TODO Depends on cc.py
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Testing",
)

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=PACKAGES,
    py_modules=MODULES,
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite=TEST_SUITE,
    entry_points=ENTRY_POINTS,
    classifiers=CLASSIFIERS,
    url=URL,
)