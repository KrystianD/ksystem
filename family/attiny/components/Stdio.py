from typing import List

import cgen

from common.component import IComponent
from family.attiny.config import StdioConfig


class DummyStdioComponent(IComponent):
    def get_header_includes(self) -> List[str]:
        return [
            "dummy_stdio.h",
        ]


class StdioComponent(IComponent):
    def __init__(self, stdio_config: StdioConfig):
        self.stdio_config = stdio_config

    def get_source_includes(self) -> List[str]:
        return [
        ]

    def get_header_includes(self) -> List[str]:
        return [
            "stdio.h",
        ]

    def emit_extern_global_variables(self, source_file):
        pass

    def emit_global_variables(self, source_file):
        source_file.add(cgen.Statement(f"""
FILE uart_stdout = {{
        .buf = 0,
        .unget = 0,
        .flags = _FDEV_SETUP_RW,
        .size = 0,
        .len = 0,
        .put = [](char c, struct __file*) {{ 
            if (c == '\\n')
                {self.stdio_config.serial}.put('\\r');
            if (c != '\\r')
                {self.stdio_config.serial}.put(c);
            return 1;
        }},
        .get = nullptr,
        .udata = nullptr,
}}"""))
        source_file.add(cgen.Line())

    def emit_helper_functions(self, source_file):
        pass

    def emit_initialization(self, source_file):
        source_file.add(cgen.Line())
        source_file.add(cgen.LineComment(f"Setup stdio"))
        source_file.add(cgen.Statement(f"stdout = &uart_stdout"))

    def emit_loop(self, source_file):
        pass

    def get_additional_linked_libraries(self) -> List[str]:
        return [
            "-Wl,-u,vfprintf",
            "-lprintf_flt",
            "-lm",
        ]
