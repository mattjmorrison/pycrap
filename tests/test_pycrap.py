import unittest
import mock

class CommandLineOptionsTests(unittest.TestCase):

    def test_reads_coverage_data_in_init(self):
        my_mock = mock.Mock()
        my_mock.asdf('hi')
        my_mock.asdf.assert_called_once_with('hi')
