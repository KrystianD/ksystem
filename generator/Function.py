import cgen as c

from generator.StatementsContainer import StatementsContainer


class Function(StatementsContainer):
    def __init__(self, sourcefile, ret_type: str, name: str):
        super().__init__()
        self.sourcefile = sourcefile
        self.ret_type = ret_type
        self.name = name

    def __enter__(self):
        return self

    def __exit__(self, *args):
        func = c.FunctionBody(
                c.FunctionDeclaration(c.Value(self.ret_type, self.name), []),
                c.Block(self.statements)
        )

        self.sourcefile.objects.append(func)
