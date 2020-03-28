import cgen as c


class Function:
    def __init__(self, sourcefile, ret_type: str, name: str):
        self.sourcefile = sourcefile
        self.ret_type = ret_type
        self.name = name
        self.statements = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        func = c.FunctionBody(
                c.FunctionDeclaration(c.Value(self.ret_type, self.name), []),
                c.Block(self.statements)
        )

        self.sourcefile.objects.append(func)

    def add(self, statement):
        if isinstance(statement, list):
            for x in statement:
                self.statements.append(x)
        else:
            self.statements.append(statement)

    def add_blank(self):
        self.add(c.Line())
