try:
    import argparse
    parser_class = argparse.ArgumentParser
except ImportError:
    import optparse
    parser_class = optparse.OptionParser

__version__ = '0.0.1'

USAGE = """
Run coverage first (ie: coverage run tests.py)
then run "pycrap"
"""

parser = parser_class(usage=USAGE)

def run():
    parser.parse_args()