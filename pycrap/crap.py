import inspect
from pycrap.support import partial
import re
from coverage import data

BLANK_REGEX = re.compile(r"\s*(#|$)").match

class ModuleInfo(object):
    def __init__(self, classes, functions):
        self.classes = classes
        self.functions = functions

class FunctionInfo(object):
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines

class MethodInfo(object):
    def __init__(self, klass, name, lines):
        self.klass = klass
        self.name = name
        self.lines = lines

class ClassInfo(object):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

class PyCrap(object):

    def _get_coverage_data(self):
        coverage_data = data.CoverageData()
        coverage_data.read()
        return coverage_data.line_data()

    def _describe(self, mod):
        mod_attr = partial(getattr, mod)
        mod_attr_names = dir(mod)

        _isclass = lambda name : inspect.isclass(mod_attr(name))
        _desc_class = lambda name : self._describe_class(mod_attr(name))

        _isfunction = lambda name : inspect.isfunction(mod_attr(name))
        _desc_function = lambda name : self._describe_function(mod_attr(name))

        classes = map(_desc_class, filter(_isclass, mod_attr_names))
        functions = map(_desc_function, filter(_isfunction, mod_attr_names))

        return ModuleInfo(classes, functions)

    def _describe_class(self, klass):
        class_attr = partial(getattr, klass)
        is_method = lambda name: inspect.ismethod(class_attr(name)) or inspect.isfunction(class_attr(name))
        desc_method = partial(self._describe_method, klass)
        methods = map(desc_method, map(class_attr, filter(is_method, dir(klass))))
        return ClassInfo(klass.__name__, list(methods))

    def _describe_method(self, klass, method):
        return MethodInfo(klass, method.__name__, self._get_line_number_range(method))

    def _describe_function(self, function):
        return FunctionInfo(function.__name__, self._get_line_number_range(function))

    def _get_line_number_range(self, obj):
        lines, starting_line = inspect.getsourcelines(obj)
        code = filter(lambda item: not BLANK_REGEX(item[1]), enumerate(lines))
        return map(lambda item: (item[0] + starting_line, item[1]), code)