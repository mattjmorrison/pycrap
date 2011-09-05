import inspect
from pycrap.support import partial
import re
from coverage import data

from import_file import import_file

BLANK_REGEX = re.compile(r"\s*(#|$)").match

class ModuleInfo(object):
    def __init__(self, classes, functions):
        self.classes = classes
        self.functions = functions

class FunctionInfo(object):
    def __init__(self, name, lines, covered_lines):
        self.name = name
        self.lines = lines
        self.covered_lines = covered_lines

    @property
    def coverage(self):
        covered_lines = filter(lambda line: line[0] in self.covered_lines, self.lines)
        return (float(len(list(covered_lines))) / float(len(self.lines))) * 100

class MethodInfo(FunctionInfo):
    def __init__(self, klass, name, lines, covered_lines):
        self.klass = klass
        self.name = name
        self.lines = lines
        self.covered_lines = covered_lines

class ClassInfo(object):
    def __init__(self, name, methods, covered_lines):
        self.name = name
        self.methods = methods
        self.covered_lines = covered_lines

class PyCrap(object):

    def get_crap(self):
        results = self._get_coverage_data()
        return list(map(self._describe, results.items()))

    def _get_coverage_data(self):
        coverage_data = data.CoverageData()
        coverage_data.read()
        return coverage_data.line_data()

    def _describe(self, coverage_data):
        mod, covered_lines = coverage_data

        if mod.endswith('setup.py'):
            # since setup.py does import time crap...
            return

        print(mod)
        module = import_file(mod)

        mod_attr = partial(getattr, module)
        mod_attr_names = dir(module)

        _isclass = lambda name : inspect.isclass(mod_attr(name))
        _desc_class = lambda name : self._describe_class(mod_attr(name), covered_lines)

        _isfunction = lambda name : inspect.isfunction(mod_attr(name))
        _desc_function = lambda name : self._describe_function(mod_attr(name), covered_lines)

        classes = map(_desc_class, filter(_isclass, mod_attr_names))
        functions = map(_desc_function, filter(_isfunction, mod_attr_names))

        return ModuleInfo(classes, functions)

    def _describe_class(self, klass, covered_lines):
        class_attr = partial(getattr, klass)
        is_method = lambda name: inspect.ismethod(class_attr(name)) or inspect.isfunction(class_attr(name))
        desc_method = partial(self._describe_method, klass, covered_lines)
        methods = map(desc_method, map(class_attr, filter(is_method, dir(klass))))
        return ClassInfo(klass.__name__,
                         list(methods),
                         covered_lines)

    def _describe_method(self, klass, covered_lines, method):
        return MethodInfo(klass,
                          method.__name__,
                          self._get_line_number_range(method),
                          covered_lines)

    def _describe_function(self, function, covered_lines):
        return FunctionInfo(function.__name__,
                            self._get_line_number_range(function),
                            covered_lines)

    def _get_line_number_range(self, obj):
        lines, starting_line = inspect.getsourcelines(obj)
        code = filter(lambda item: not BLANK_REGEX(item[1]), enumerate(lines))
        return map(lambda item: (item[0] + starting_line, item[1]), code)