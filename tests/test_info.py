import unittest
import mock
from pycrap import info

CLASS_DEF = [
    (100, 'class Something(object):'),
    (102, '    def __init__(self):'),
    (103, '        self.something = []'),
    (105, '    def show_me(self):'),
    (106, '        for thing in self.something:'),
    (107, '            yield thing'),
]

FUNCTION_DEF = [
    (100, 'def create_new_plant(name):\n'),
    (102, '    new_plant = Plant(name)\n'),
    (104, '    for _ in range(10):\n'),
    (105, '        new_plant.photosynthesize()\n'),
    (107, '    return new_plant\n'),
]

class FunctionInfoTests(unittest.TestCase):
    def setUp(self):
        self.info = info.FunctionInfo('name',
            [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')], (1, 2, 4))

    def test_complexity(self):
        func_info = info.FunctionInfo('name', FUNCTION_DEF, (100, 102))
        self.assertEqual(2, func_info.complexity)

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

    def test_complexity(self):
        class_info = info.ClassInfo('name', self.methods, (105, 106))
        self.assertEqual(2, class_info.complexity)

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
