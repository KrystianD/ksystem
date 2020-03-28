from typing import List, Tuple

import cgen

from components.component import IComponent
from config import GPIOPinDef


class GPIOComponent(IComponent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.gpio = self.cfg.components.gpio

        self.definitions: List[Tuple[str, GPIOPinDef]] = [(list(x)[0], x[list(x)[0]]) for x in self.gpio]

    def get_source_includes(self) -> List[str]:
        return [
            "avr/io.h",
        ]

    def get_header_includes(self) -> List[str]:
        return [
            "kGPIO.h",
        ]

    def emit_extern_global_variables(self, source_file):
        source_file.add(cgen.Pragma("""push_macro("_SFR_IO8")"""))
        source_file.add(cgen.Line("#undef _SFR_IO8"))
        source_file.add(cgen.Define("_SFR_IO8(x)", "x"))

        for name, definition in self.definitions:
            port = definition.port[0]
            assert port in ("A", "B", "C", "D", "E")
            pin = int(definition.port[1])

            source_file.add(cgen.Statement(f"static kGPIO<PORT{port},{pin}> {name}"))

        source_file.add(cgen.Pragma("""pop_macro("_SFR_IO8")"""))

    def emit_global_variables(self, source_file):
        pass

    def emit_helper_functions(self, source_file):
        pass

    def emit_initialization(self, source_file):
        for name, definition in self.definitions:
            if definition.mode == "push-pull":
                source_file.add(cgen.Statement(f"{name}.pushPull()"))

            if definition.value is True:
                source_file.add(cgen.Statement(f"{name}.high()"))

    def emit_loop(self, source_file):
        pass
