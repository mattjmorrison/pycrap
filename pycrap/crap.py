import inspect
import re
from import_file import import_file
from coverage import data
from pycrap.support import partial

BLANK_REGEX = re.compile(r"\s*(#|$)").match

class CoverageInfo(object):

    def __init__(self):
        self.lines = []
        self.covered_lines = []

    @property
    def covered(self):
        return [line for line in self.lines if line[0] in self.covered_lines]

    @property
    def coverage(self):
        covered_lines = filter(lambda line: line[0] in self.covered_lines, self.lines)
        return (float(len(list(covered_lines))) / float(len(self.lines))) * 100

class ModuleInfo(object):

    def __init__(self, classes, functions, covered_lines):
        self.classes = classes
        self.functions = functions
        self.covered_lines = covered_lines

    @property
    def lines(self):
        results = []
        append_lines = lambda info: results.extend(info.lines)
        # python 3 is lazy
        list(map(append_lines, self.classes))
        list(map(append_lines, self.functions))

        return list(sorted(results))

    @property
    def coverage(self):
        class_coverage = sum(klass.coverage for klass in self.classes)
        func_coverage = sum(func.coverage for func in self.functions)
        return class_coverage + func_coverage

class FunctionInfo(CoverageInfo):

    def __init__(self, name, lines, covered_lines):
        self.name = name
        self.lines = lines
        self.covered_lines = covered_lines

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

    @property
    def lines(self):
        results = []
        #python 3 is lazy
        list(map(lambda method: results.extend(method.lines), self.methods))
        return list(results)

    @property
    def coverage(self):
        return sum(method.coverage for method in self.methods)

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

        return ModuleInfo(classes, functions, coverage_data)

    def _describe_class(self, klass, covered_lines):
        class_attr = partial(getattr, klass)
        is_method = lambda name: inspect.ismethod(class_attr(name)) or inspect.isfunction(class_attr(name))
        desc_method = partial(self._describe_method, klass, covered_lines)
        methods = map(desc_method, map(class_attr, filter(is_method, dir(klass))))
        return ClassInfo(klass.__name__, list(methods), covered_lines)

    def _describe_method(self, klass, covered_lines, method):
        return MethodInfo(klass, method.__name__, self._get_line_number_range(method), covered_lines)

    def _describe_function(self, function, covered_lines):
        return FunctionInfo(function.__name__, self._get_line_number_range(function), covered_lines)

    def _get_line_number_range(self, obj):
        lines, starting_line = inspect.getsourcelines(obj)
        code = filter(lambda item: not BLANK_REGEX(item[1]), enumerate(lines))
        return map(lambda item: (item[0] + starting_line, item[1]), code)
