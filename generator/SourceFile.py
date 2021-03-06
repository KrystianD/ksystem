import cgen
import cgen as c

from generator.Function import Function
from generator.IStatementsContainer import IStatementsContainer


class SourceFile(IStatementsContainer):
    def __init__(self, is_header: bool):
        self.includes = []
        self.objects = []

        if is_header:
            self.add(cgen.Pragma("once"))
        # self.objects += [c.Include(x) for x in includes]

    def add_include(self, path: str, system: bool):
        self.includes.append(c.Include(path, system))

    def function(self, ret_type: str, name: str):
        return Function(self, ret_type, name)

    def generate(self):
        objects = []
        objects += self.includes
        objects += [c.Line()]
        objects += self.objects

        return "\n".join(str(x) for x in objects)

    def add(self, statement):
        if isinstance(statement, list):
            for x in statement:
                self.objects.append(x)
        else:
            self.objects.append(statement)

    def save(self, path: str):
        with open(path, "wt") as f:
            f.write(self.generate())
