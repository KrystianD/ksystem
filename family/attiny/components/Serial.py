from typing import List

import cgen

from common.component import IComponent
from family.attiny.config import Config, SerialConfig
from family.attiny.hardware.serial import configure_serial


class SerialComponent(IComponent):
    def __init__(self, name: str, cfg: Config, serial_cfg: SerialConfig):
        self.name = name
        self.cfg = cfg
        self.serial_cfg = serial_cfg

    def get_source_includes(self) -> List[str]:
        return [
            "avr/io.h",
            "avr/interrupt.h",
        ]

    def get_header_includes(self) -> List[str]:
        return [
            "kSerial.h",
            "kGPIO.h",
        ]

    def emit_extern_global_variables(self, source_file):
        usart_dev = self.serial_cfg.usart

        source_file.add(cgen.Statement(f"static kSerial<k{usart_dev}> {self.name}"))

    def emit_global_variables(self, source_file):
        pass

    def emit_helper_functions(self, source_file):
        pass

    def emit_initialization(self, source_file):
        source_file.add(configure_serial(self.cfg, self.serial_cfg))

    def emit_loop(self, source_file):
        pass

    def get_interrupt_RXC(self):
        return f"{self.serial_cfg.usart}_RXC"

    def get_interrupt_DRE(self):
        return f"{self.serial_cfg.usart}_DRE"

    def get_interrupt_TXC(self):
        return f"{self.serial_cfg.usart}_TXC"
