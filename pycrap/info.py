
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

class ModuleInfo(CoverageInfo):

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

class ClassInfo(CoverageInfo):

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
