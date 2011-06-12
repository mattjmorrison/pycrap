# Copyright (C) 2011 Matthew J. Morrison
# E-mail: mattjmorrison AT mattjmorrison DOT com

from setuptools import setup

from crap import __version__
import os

NAME = "pycrap"
AUTHOR = 'Matthew J. Morrison'
AUTHOR_EMAIL = 'mattjmorrison@mattjmorrison.com'
URL = 'http://www.pycrap.com'
DESCRIPTION = "A Python code Change Risk Analyzer and Predictor (a.k.a. CRAP)"
readme = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(readme).read()

MODULES = ('pycrap',)
REQUIREMENTS = ('coverage', 'import_file', ) #'pygenie'
ENTRY_POINTS = {'console_scripts': ['pycrap = crap:run']}
CLASSIFIERS = (
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Testing",
)

setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    py_modules=MODULES,
    install_requires=REQUIREMENTS,
    entry_points=ENTRY_POINTS,
    classifiers=CLASSIFIERS,
    url=URL,
)