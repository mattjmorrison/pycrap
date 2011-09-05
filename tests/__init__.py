import unittest
from tests import test_info, test_pycrap

SUITE = unittest.TestLoader().loadTestsFromModule(test_info)
SUITE.addTests(unittest.TestLoader().loadTestsFromModule(test_pycrap))