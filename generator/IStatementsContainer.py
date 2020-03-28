from abc import abstractmethod

import cgen as c


class IStatementsContainer:
    @abstractmethod
    def add(self, statement): ...

    def add_blank(self):
        self.add(c.Line())
