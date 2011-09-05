import inspect
import re
from import_file import import_file
from coverage import data
from pycrap.support import partial
from pycrap import info

BLANK_REGEX = re.compile(r"\s*(#|$)").match

class PyCrap(object):

    def get_crap(self):
        results = self._get_coverage_data()
        # python 3 is lazy
        return list(map(self._describe, results.items()))

    def _get_coverage_data(self):
        coverage_data = data.CoverageData()
        coverage_data.read()
        return coverage_data.line_data()

    def _describe(self, coverage_data):
        mod, covered_lines = coverage_data

        module = import_file(mod)

        mod_attr = partial(getattr, module)
        mod_attr_names = dir(module)

        _isclass = lambda name : inspect.isclass(mod_attr(name))
        _desc_class = lambda name : self._describe_class(mod_attr(name), covered_lines)

        _isfunction = lambda name : inspect.isfunction(mod_attr(name))
        _desc_function = lambda name : self._describe_function(mod_attr(name), covered_lines)

        classes = map(_desc_class, filter(_isclass, mod_attr_names))
        functions = map(_desc_function, filter(_isfunction, mod_attr_names))

        return info.ModuleInfo(classes, functions, coverage_data)

    def _describe_class(self, klass, covered_lines):
        class_attr = partial(getattr, klass)
        is_method = lambda name: inspect.ismethod(class_attr(name)) or inspect.isfunction(class_attr(name))
        desc_method = partial(self._describe_method, klass, covered_lines)
        methods = map(desc_method, map(class_attr, filter(is_method, dir(klass))))
        return info.ClassInfo(klass.__name__, list(methods), covered_lines)

    def _describe_method(self, klass, covered_lines, method):
        return info.MethodInfo(klass, method.__name__, self._get_line_number_range(method), covered_lines)

    def _describe_function(self, function, covered_lines):
        return info.FunctionInfo(function.__name__, self._get_line_number_range(function), covered_lines)

    def _get_line_number_range(self, obj):
        lines, starting_line = inspect.getsourcelines(obj)
        code = filter(lambda item: not BLANK_REGEX(item[1]), enumerate(lines))
        return map(lambda item: (item[0] + starting_line, item[1]), code)
