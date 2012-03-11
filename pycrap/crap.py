import inspect
from functools import partial
import re
import cc
import math
from coverage import data

from import_file import import_file

BLANK_REGEX = re.compile(r"\s*(#|$)").match

def crap(coverage, complexity):
    return complexity * (complexity * (math.pow(1.0 - (coverage / 100), 3.0))) + complexity

class ModuleInfo(object):
    def __init__(self, classes, functions):
        self.classes = classes
        self.functions = functions

    @property
    def coverage(self):
        function_coverage = sum([func.coverage for func in self.functions])
        class_coverage = sum([klass.coverage for klass in self.classes])
        return sum((function_coverage, class_coverage)) / (len(self.classes) + len(self.functions))

    @property
    def complexity(self):
        function_complexity = sum([func.complexity for func in self.functions])
        class_complexity = sum([klass.complexity for klass in self.classes])
        return sum([function_complexity, class_complexity])
        
    @property
    def crap(self):
        return crap(self.coverage, self.complexity)

class ClassInfo(object):
    def __init__(self, name, methods, covered_lines):
        self.name = name
        self.methods = methods
        self.covered_lines = covered_lines

    @property
    def coverage(self):
        return sum([method.coverage for method in self.methods]) / len(self.methods)

    @property
    def complexity(self):
        return sum([method.complexity for method in self.methods])
        
    @property
    def crap(self):
        return crap(self.coverage, self.complexity)

class FunctionInfo(object):
    def __init__(self, name, lines, covered_lines):
        self.name = name
        self.lines = lines
        self.covered_lines = covered_lines

    @property
    def coverage(self):
        covered_lines = filter(lambda line: line[0] in self.covered_lines, self.lines)
        return (float(len(list(covered_lines))) / float(len(self.lines))) * 100

    @property
    def complexity(self):
        return cc.measure_complexity(''.join([''.join(line[1]) for line in self.lines])).functions[0].complexity

    @property
    def crap(self):
        return crap(self.coverage, self.complexity)

class MethodInfo(FunctionInfo):
    def __init__(self, klass, name, lines, covered_lines):
        self.klass = klass
        self.name = name
        self.lines = lines
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
        return ClassInfo(klass.__name__, list(methods), covered_lines)

    def _describe_method(self, klass, covered_lines, method):
        return MethodInfo(klass, method.__name__, self._get_line_number_range(method), covered_lines)

    def _describe_function(self, function, covered_lines):
        return FunctionInfo(function.__name__, self._get_line_number_range(function), covered_lines)

    def _get_line_number_range(self, obj):
        lines, starting_line = inspect.getsourcelines(obj)
        code = filter(lambda item: not BLANK_REGEX(item[1]), enumerate(lines))
        return map(lambda item: (item[0] + starting_line, item[1]), code)
        
#TODO untested

def print_report(data):
    names = ['asdf', 'xxx', 'aa', 'yyyy']
    name_format = "%%(name)-%ds" % len(max(names, key=len))
    output_string = name_format + "%(complexity)10d %(coverage)8d%% %(crap)2.2f"
    headings = (name_format + " Complexity Coverage Crap") % {'name': 'Name', }
    print headings
    print '-' * len(headings)
    # for row in data:
        # print output_string % row

if __name__ == '__main__':
    pycrap = PyCrap()
    print pycrap.get_crap()
    # print_report()
