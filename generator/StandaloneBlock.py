import cgen
import cgen as c

from generator.IStatementsContainer import IStatementsContainer
from generator.SourceFile import SourceFile
from generator.StatementsContainer import StatementsContainer


class StandaloneBlock(StatementsContainer):
    def __init__(self, sourcefile: IStatementsContainer):
        super().__init__()
        self.sourcefile = sourcefile

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.sourcefile.add(c.Block(self.statements))
