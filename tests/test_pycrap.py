import unittest
import mock

import os
import inspect

from pycrap import crap

from tests.sample_app import life

FUNCTION_DEF = [
    (100, 'def create_new_plant(name):\n'),
    (102, '    new_plant = Plant(name)\n'),
    (104, '    for _ in range(10):\n'),
    (105, '        new_plant.photosynthesize()\n'),
    (107, '    return new_plant\n'),
]

class FunctionInfoTests(unittest.TestCase):
    def setUp(self):
        self.info = crap.FunctionInfo('name',
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
        self.info = crap.MethodInfo(mock.Mock(),
            'name',
            [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')], (1, 2, 4))

class ClassInfoTests(unittest.TestCase):

    def setUp(self):
        self.methods = [
            crap.MethodInfo(
                mock.Mock(),
                'name',
                [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')],
                (1, 2, 4)),
            crap.MethodInfo(
                mock.Mock(),
                'name',
                [(5, 'a'), (6, 'b'), (7, 'c'), (8, 'd')],
                (1, 2, 4)),
        ]
        self.info = crap.ClassInfo('sample', self.methods, (1, 2, 4))

    def test_coverage_percent(self):
        self.assertEqual(75, self.info.coverage)

    def test_lines_aggregates_functions_methods(self):
        self.assertEqual([
            (1, 'a'), (2, 'b'), (3, 'c'), (4, 'd'),
            (5, 'a'), (6, 'b'), (7, 'c'), (8, 'd'),
        ], self.info.lines)

class ModuleInfoTests(unittest.TestCase):

    def setUp(self):
        coverage_info = (1, 2, 4, 5, 6, 8)

        self.functions = [
            crap.FunctionInfo(
                'name',
                [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')],
                coverage_info),
        ]

        self.methods = [
            crap.MethodInfo(
                mock.Mock(),
                'name',
                [(5, 'a'), (6, 'b'), (7, 'c'), (8, 'd')],
                coverage_info),
        ]

        self.classes = [
            crap.ClassInfo(
                'name',
                self.methods,
                coverage_info
            )
        ]

        self.info = crap.ModuleInfo(self.classes, self.functions, coverage_info)

    def _test_coverage_percent(self):
        self.assertEqual(75, self.info.coverage)

    def test_lines_aggregates_classes_and_functions(self):
        self.assertEqual([
            (1, 'a'), (2, 'b'), (3, 'c'), (4, 'd'),
            (5, 'a'), (6, 'b'), (7, 'c'), (8, 'd'),
        ], self.info.lines)

class PycrapTests(unittest.TestCase):

    def get_file_path_for_module(self, module):
        file_path = os.path.abspath(module.__file__)
        if file_path.endswith('$py.class'): #jython
            file_path = file_path[:-9] + ".py"
        return file_path

    @mock.patch('coverage.data.CoverageData')
    def test_reads_coverage_data_in_get_coverage_data(self, coverage_data_class):
        pycrap = crap.PyCrap()
        coverage_data = coverage_data_class.return_value
        data = pycrap._get_coverage_data()
        coverage_data.read.assert_called_once_with()
        self.assertEqual(coverage_data.line_data.return_value, data)

    def test_describes_files_in_coverage_data(self):
        pycrap_instance = mock.Mock(spec_set=crap.PyCrap)
        somefile_data = mock.Mock()
        another_file_data = mock.Mock()
        coverage_data = {'somefile.py': somefile_data,
                         'another_file.py': another_file_data}
        pycrap_instance._get_coverage_data.return_value = coverage_data
        crap.PyCrap.get_crap(pycrap_instance)

        # sort these because calls are made in order of dict keys
        self.assertEqual(
            sorted([
                ((('somefile.py', somefile_data),), {}),
                ((('another_file.py', another_file_data),), {})
            ]), sorted(pycrap_instance._describe.call_args_list))

    def test_gets_line_number_range_for_given_function(self):
        pycrap = crap.PyCrap()
        result = pycrap._get_line_number_range(life.create_new_plant)
        self.assertEqual(FUNCTION_DEF, list(result))

    def test_gets_data_for_function_in_describe_function(self):
        pycrap = crap.PyCrap()
        function_data = pycrap._describe_function(life.create_new_plant, [])
        self.assertEqual('create_new_plant', function_data.name)
        self.assertEqual(FUNCTION_DEF, list(function_data.lines))

    def test_gets_data_for_method_in_describe_method(self):
        pycrap = crap.PyCrap()
        method_data = pycrap._describe_method(
            life.Person, [], life.Person.can_drink)
        self.assertEqual(life.Person, method_data.klass)
        self.assertEqual('can_drink', method_data.name)
        self.assertEqual([
            (8, "    def can_drink(self, liquid):\n"),
            (9, "        return liquid in self.drinks\n"),
        ], list(method_data.lines))
        

    def test_calls_describe_function_for_functions_in_describe(self):
        instance = mock.Mock(spec=crap.PyCrap())
        result = crap.PyCrap._describe(instance, life)
        list(result.functions)
        instance._describe_function.assert_called_once_with(life.create_new_plant)

    def test_calls_describe_class_for_classes_in_describe(self):
        instance = mock.Mock(spec=crap.PyCrap())
        result = crap.PyCrap._describe(instance, life)
        list(result.classes)
        self.assertEqual([
            mock.call(life.Animal),
            mock.call(life.ComputerProgrammer),
            mock.call(life.Dog),
            mock.call(life.Fish),
            mock.call(life.HouseCat),
            mock.call(life.Life),
            mock.call(life.Person),
            mock.call(life.Plant),
        ], instance._describe_class.call_args_list)

    def test_calls_describe_method_for_methods_in_describe(self):
        instance = mock.Mock(spec=crap.PyCrap())
        crap.PyCrap._describe_class(instance, life.Life)
        self.assertEqual([
            mock.call(life.Life, life.Life.__init__),
            mock.call(life.Life, life.Life.can_drink),
            mock.call(life.Life, life.Life.can_eat),
        ], instance._describe_method.call_args_list)

    def test_describe_returns_module_info(self):
        instance = mock.Mock(spec=crap.PyCrap())
        module_info = crap.PyCrap._describe(instance, life)

    def test_calls_describe_function_for_functions_in_describe(self):
        file_path = self.get_file_path_for_module(life)
        instance = mock.Mock(spec=crap.PyCrap())
        coverage_data = mock.Mock()
        result = crap.PyCrap._describe(instance, (file_path, coverage_data))
        list(result.functions)
        self.assertEqual(1, instance._describe_function.call_count)
        call_args = instance._describe_function.call_args
        self.assertTrue(inspect.isfunction(call_args[0][0]))
        self.assertEqual(coverage_data, call_args[0][1])

    def test_calls_describe_class_for_classes_in_describe(self):
        file_path = self.get_file_path_for_module(life)
        coverage_data = mock.Mock()
        instance = mock.Mock(spec=crap.PyCrap())
        result = crap.PyCrap._describe(instance, (file_path, coverage_data))
        list(result.classes)

        for call_arg in instance._describe_class.call_args_list:
            self.assertTrue(inspect.isclass(call_arg[0][0]))
            self.assertEqual(coverage_data, call_arg[0][1])
            self.assertEqual(2, len(call_arg[0]))

    def test_calls_describe_method_for_methods_in_describe(self):
        instance = mock.Mock(spec=crap.PyCrap())
        crap.PyCrap._describe_class(instance, life.Life, [])
        self.assertEqual([
            ((life.Life, [], life.Life.__init__), {}),
            ((life.Life, [], life.Life.can_drink), {}),
            ((life.Life, [], life.Life.can_eat), {}),
        ], instance._describe_method.call_args_list)

    def test_describe_returns_module_info(self):
        file_path = self.get_file_path_for_module(life)
        instance = mock.Mock(spec=crap.PyCrap())
        module_info = crap.PyCrap._describe(instance, (file_path, mock.Mock()))

        self.assertEqual(8, len(list(module_info.classes)))
        self.assertEqual(1, len(list(module_info.functions)))

    def test_describe_class_returns_class_info(self):
        instance = mock.Mock(spec=crap.PyCrap())
        class_info = crap.PyCrap._describe_class(instance, life.Life, [])
        self.assertEqual('Life', class_info.name)
        self.assertEqual(3, len(class_info.methods))
        self.assertEqual([instance._describe_method()] * 3, class_info.methods)
