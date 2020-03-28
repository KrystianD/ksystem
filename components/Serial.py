from typing import List

import cgen

from components.component import IComponent
from hardware.serial import configure_serial


class SerialComponent(IComponent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.serial = self.cfg.components.serial

    def get_source_includes(self) -> List[str]:
        return [
            "avr/io.h",
            "avr/interrupt.h",
        ]

    def get_header_includes(self) -> List[str]:
        return [
            "stdio.h" if self.serial.stdio else None,
            "kSerial.h",
        ]

    def emit_extern_global_variables(self, source_file):
        source_file.add(cgen.Statement(f"static kSerial Serial"))

    def emit_global_variables(self, source_file):
        if self.serial.stdio:
            source_file.add(cgen.Statement("""
FILE uart_stdout = {
        .buf = 0,
        .unget = 0,
        .flags = _FDEV_SETUP_RW,
        .size = 0,
        .len = 0,
        .put = [](char c, struct __file*) { Serial.put(c); return 1; },
        .get = nullptr,
        .udata = nullptr,
}"""))
            source_file.add(cgen.Line())

    def emit_helper_functions(self, source_file):
        pass

    def emit_initialization(self, source_file):
        source_file.add(configure_serial(self.cfg, self.serial.baudrate))

        if self.serial.stdio:
            source_file.add(cgen.Line())
            source_file.add(cgen.LineComment(f"Setup stdio"))
            source_file.add(cgen.Statement(f"stdout = &uart_stdout"))

    def emit_loop(self, source_file):
        pass
