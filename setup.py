"""
Copyright (C) 2011 Matthew J. Morrison
E-mail: mattjmorrison AT mattjmorrison DOT com
"""
from setuptools import setup
from os import path

README = path.join(path.dirname(__file__), 'README.txt')

setup(
    name="pycrap",
    version='0.0.1',
    description="A Python code Change Risk Analyzer and Predictor (a.k.a. CRAP)",
    long_description=open(README).read(),
    author='Matthew J. Morrison',
    author_email='mattjmorrison@mattjmorrison.com',
    packages=('pycrap', ),
    py_modules=('cc', 'pygenie', ),
    install_requires=('coverage', 'import_file', ),
    tests_require=('mock', ),
    test_suite='tests.SUITE',
    entry_points={'console_scripts': [
        'pycrap = pycrap:run',
        'pygenie = pygenie:main'
    ]},
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        #Jython classifier?
        #pypy ??? WTF? Why Can't I get this mofo running?
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
    ),
    url='http://www.pycrap.com',
)