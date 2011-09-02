import unittest
import mock

from pycrap import crap

from tests.sample_app import life

FUNCTION_DEF = [
    (100, 'def create_new_plant(name):\n'),
    (102, '    new_plant = Plant(name)\n'),
    (104, '    for _ in range(10):\n'),
    (105, '        new_plant.photosynthesize()\n'),
    (107, '    return new_plant\n'),
]

class PycrapTests(unittest.TestCase):

    @mock.patch('coverage.data.CoverageData')
    def test_reads_coverage_data_in_get_coverage_data(self, coverage_data_class):
        pycrap = crap.PyCrap()
        coverage_data = coverage_data_class.return_value
        data = pycrap._get_coverage_data()
        coverage_data.read.assert_called_once_with()
        self.assertEqual(coverage_data.line_data.return_value, data)

# import imp
# foo = imp.load_source('module.name', '/path/to/file.py')
#TODO strip out 'file' to use as the name... this should work.

#    @mock.patch('pycrap.crap.PyCrap._get_coverage_data')
#    def test_describes_files_in_coverage_data(self, _get_coverage_data):
#        pycrap_instance = mock.Mock(spec_set=crap.PyCrap)
#        _get_coverage_data.return_value.items.return_value = {'filename': mock.Mock()}
#        crap.PyCrap.get_crap(pycrap_instance)
#        pycrap_instance._describe.assert_called_once_with('filename')

    def test_gets_line_number_range_for_given_function(self):
        pycrap = crap.PyCrap()
        result = pycrap._get_line_number_range(life.create_new_plant)
        self.assertEqual(FUNCTION_DEF, list(result))

    def test_gets_data_for_function_in_describe_function(self):
        pycrap = crap.PyCrap()
        function_data = pycrap._describe_function(life.create_new_plant)
        self.assertEqual('create_new_plant', function_data.name)
        self.assertEqual(FUNCTION_DEF, list(function_data.lines))

    def test_gets_data_for_method_in_describe_method(self):
        pycrap = crap.PyCrap()
        method_data = pycrap._describe_method(life.Person, life.Person.can_drink)
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
        self.assertEqual(8, len(list(module_info.classes)))
        self.assertEqual(1, len(list(module_info.functions)))

    def test_describe_class_returns_class_info(self):
        instance = mock.Mock(spec=crap.PyCrap())
        class_info = crap.PyCrap._describe_class(instance, life.Life)
        self.assertEqual('Life', class_info.name)
        self.assertEqual(3, len(class_info.methods))
        self.assertEqual([instance._describe_method()] * 3, class_info.methods)
