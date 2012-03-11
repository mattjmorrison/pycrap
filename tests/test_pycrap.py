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

METHOD_DEFS = [
    crap.MethodInfo(mock.Mock(), 'first', FUNCTION_DEF, (100, 102, 104)),
    crap.MethodInfo(mock.Mock(), 'second', FUNCTION_DEF, (100, 102, 104)),
]

FUNC_DEFS = [
    crap.FunctionInfo('name', FUNCTION_DEF, (100, 102, 104)),
    crap.FunctionInfo('name', FUNCTION_DEF, (100, 102, 104)),
]

CLASS_DEFS = [
    crap.ClassInfo('name', METHOD_DEFS, (1, 2, 3)),
    crap.ClassInfo('name', METHOD_DEFS, (1, 2, 3)),
]

class InfoTests(object):

    def test_coverage_percent(self):
        self.assertEqual(60, self.info.coverage)    

class FunctionInfoTests(InfoTests, unittest.TestCase):

    def setUp(self):
        self.info = crap.FunctionInfo('name', FUNCTION_DEF, (100, 102, 104))
        
    def test_complexity_number(self):
        self.assertEqual(2, self.info.complexity)
        
    def test_crap_number(self):
        self.assertAlmostEqual(2.26, self.info.crap, 2)

class MethodInfoTests(FunctionInfoTests):

    def setUp(self):
        self.info = crap.MethodInfo(mock.Mock(), 'name', FUNCTION_DEF, (100, 102, 104))

class ClassInfoTests(InfoTests, unittest.TestCase):

    def setUp(self):
        self.info = crap.ClassInfo('name', METHOD_DEFS, (200, 201, 204))

    def test_complexity_number(self):
        self.assertEqual(4, self.info.complexity)
        
    def test_crap_number(self):
        self.assertAlmostEqual(5.02, self.info.crap, 2)

class ModuleInfoTests(InfoTests, unittest.TestCase):

    def setUp(self):
        self.info = crap.ModuleInfo(CLASS_DEFS, FUNC_DEFS)

    def test_complexity_number(self):
        self.assertEqual(12, self.info.complexity)
        
    def test_crap_number(self):
        self.assertAlmostEqual(21.22, self.info.crap, 2)

class PycrapTests(unittest.TestCase):

    def get_file_path_for_module(self, module):
        file_path = os.path.abspath(module.__file__)
        if file_path.endswith('$py.class'):
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
        
class CrapTests(unittest.TestCase):

    def setUp(self):
        self.complexity = [1, 4, 5, 8, 9, 16, 17]
        self.coverage = [0.0, 1.0, 20.0, 21.0, 40.0, 41.0, 60.0, 61.0, 80.0, 81.0, 99.0, 100.0]
        self.crap_results = [
            [2.0, 20.0, 30.0, 72.0, 90.0, 272.0, 306.0],
            [1.970299, 19.524784, 29.257475, 70.099136, 87.594219, 264.396544, 297.416411],
            [1.512, 12.192, 17.8, 40.768, 50.472, 147.072, 164.968],
            [1.493039, 11.888624, 17.325975, 39.554496, 48.936159, 142.217984, 159.488271],
            [1.216, 7.456, 10.4, 21.824, 26.496, 71.296, 79.424],
            [1.205379, 7.286064, 10.134475, 21.144256, 25.635699, 68.577024, 76.354531],
            [1.064, 5.024, 6.6, 12.096, 14.184, 32.384, 35.496],
            [1.059319, 4.949104, 6.482975, 11.796416, 13.804839, 31.185664, 34.143191],
            [1.008, 4.128, 5.2, 8.512, 9.648, 18.048, 19.312],
            [1.006859, 4.109744, 5.171475, 8.438976, 9.555579, 17.755904, 18.982251],
            [1.000001, 4.000016, 5.000025, 8.000064, 9.000081, 16.000256, 17.000289],
            [1.0, 4.0, 5.0, 8.0, 9.0, 16.0, 17.0]
        ]

    def test_crap_results(self):
        for coverage_index, coverage in enumerate(self.coverage):
            for complexity_index, complexity in enumerate(self.complexity):
                result = crap.crap(coverage, complexity)
                self.assertAlmostEqual(self.crap_results[coverage_index][complexity_index], result, 7)  
