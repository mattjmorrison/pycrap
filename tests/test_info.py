import unittest
import mock
from pycrap import info

class FunctionInfoTests(unittest.TestCase):
    def setUp(self):
        self.info = info.FunctionInfo('name',
            [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')], (1, 2, 4))

    def test_coverage_percent(self):
        self.assertEqual(75, self.info.coverage)

    def test_covered_lines(self):
        self.assertEqual(
            [(1, 'a'), (2, 'b'), (4, 'd')],
            self.info.covered
        )

class MethodInfoTests(FunctionInfoTests):

    def setUp(self):
        self.info = info.MethodInfo(mock.Mock(),
            'name',
            [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')], (1, 2, 4))

class ClassInfoTests(unittest.TestCase):

    def setUp(self):
        self.methods = [
            info.MethodInfo(
                mock.Mock(),
                'name',
                [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')],
                (1, 2, 4)),
            info.MethodInfo(
                mock.Mock(),
                'name',
                [(5, 'a'), (6, 'b'), (7, 'c'), (8, 'd')],
                (1, 2, 4)),
        ]
        self.info = info.ClassInfo('sample', self.methods, (1, 2, 4))

    def test_coverage_percent(self):
        self.assertEqual(37.5, self.info.coverage)

    def test_lines_aggregates_functions_methods(self):
        self.assertEqual([
            (1, 'a'), (2, 'b'), (3, 'c'), (4, 'd'),
            (5, 'a'), (6, 'b'), (7, 'c'), (8, 'd'),
        ], self.info.lines)

class ModuleInfoTests(unittest.TestCase):

    def setUp(self):
        coverage_info = (1, 2, 4, 5, 6, 8)

        self.functions = [
            info.FunctionInfo(
                'name',
                [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')],
                coverage_info),
        ]

        self.methods = [
            info.MethodInfo(
                mock.Mock(),
                'name',
                [(5, 'a'), (6, 'b'), (7, 'c'), (8, 'd')],
                coverage_info),
        ]

        self.classes = [
            info.ClassInfo(
                'name',
                self.methods,
                coverage_info
            )
        ]

        self.info = info.ModuleInfo(self.classes, self.functions, coverage_info)

    def test_coverage_percent(self):
        self.assertEqual(75, self.info.coverage)

    def test_lines_aggregates_classes_and_functions(self):
        self.assertEqual([
            (1, 'a'), (2, 'b'), (3, 'c'), (4, 'd'),
            (5, 'a'), (6, 'b'), (7, 'c'), (8, 'd'),
        ], self.info.lines)
