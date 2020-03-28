from abc import abstractmethod
from typing import List

from config import Config


class IComponent:
    def __init__(self, cfg: Config):
        self.cfg = cfg

    @abstractmethod
    def get_source_includes(self) -> List[str]: ...

    @abstractmethod
    def get_header_includes(self) -> List[str]: ...

    @abstractmethod
    def emit_extern_global_variables(self, source_file): ...

    @abstractmethod
    def emit_global_variables(self, source_file): ...

    @abstractmethod
    def emit_helper_functions(self, source_file): ...

    @abstractmethod
    def emit_initialization(self, source_file): ...

    @abstractmethod
    def emit_loop(self, source_file): ...

    def get_additional_source_files(self) -> List[str]:
        return []

    @abstractmethod
    def get_additional_header_directories(self) -> List[str]:
        return []
