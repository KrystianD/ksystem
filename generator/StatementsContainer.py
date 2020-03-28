import cgen
import cgen as c

from generator.IStatementsContainer import IStatementsContainer


class StatementsContainer(IStatementsContainer):
    def __init__(self):
        self.statements = []

    def add(self, statement):
        if isinstance(statement, str):
            self.statements.append(cgen.Statement(statement))
        elif isinstance(statement, list):
            for x in statement:
                self.statements.append(x)
        else:
            self.statements.append(statement)
