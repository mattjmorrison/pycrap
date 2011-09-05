try:
    import argparse
    parser_class = argparse.ArgumentParser
except ImportError:
    import optparse
    parser_class = optparse.OptionParser

USAGE = """
Run coverage first (ie: coverage run tests.py)
then run "pycrap"
"""

parser = parser_class(usage=USAGE)

#from pycrap import crap

def run():
    parser.parse_args()
#    print crap.PyCrap().get_crap()
