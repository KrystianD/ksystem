import os

import cgen

from common.Generator import BaseGenerator
from family.attiny.components.GPIO import GPIOComponent
from family.attiny.components.Interrupts import InterruptsComponent
from family.attiny.components.Modbus import ModbusComponent
from family.attiny.components.Serial import SerialComponent
from family.attiny.components.Stdio import StdioComponent, DummyStdioComponent
from family.attiny.components.Systick import SysTickComponent
from family.attiny.config import Config

script_dir = os.path.dirname(os.path.realpath(__file__))


class AttinyGenerator(BaseGenerator):
    def __init__(self, cfg: Config, output_dir: str):
        super().__init__(output_dir, script_dir)
        self.cfg = cfg

        self.add_global_define(f"F_CPU={self.cfg.frequency}")

        self.interrupts = InterruptsComponent()
        self.add_component(self.interrupts)

    def prepare_components(self) -> None:
        serial_by_name: dict[str, SerialComponent] = {}

        for name, serial_cfg in (self.cfg.components.serial or {}).items():
            serial = SerialComponent(name, self.cfg, serial_cfg)
            serial_by_name[serial.name] = serial
            self.add_component(serial)

        if self.cfg.components.systick:
            systick = SysTickComponent(self.cfg, self.interrupts)
            self.add_component(systick)

        if self.cfg.components.stdio is not None:
            stdio = StdioComponent(self.cfg.components.stdio)
            self.add_component(stdio)
        else:
            stdio = DummyStdioComponent()
            self.add_component(stdio)

        if self.cfg.components.gpio is not None:
            gpio = GPIOComponent(self.cfg.components.gpio, self.interrupts)
            self.add_component(gpio)

        if self.cfg.components.modbus is not None:
            gpio = ModbusComponent(self.cfg.components.modbus, self.interrupts,
                                   modbus_serial=serial_by_name[self.cfg.components.modbus.serial])
            self.add_component(gpio)

    def on_init(self, f) -> None:
        f.add(cgen.Statement("_PROTECTED_WRITE(CLKCTRL.MCLKCTRLA, 0)"))
        f.add(cgen.Statement("_PROTECTED_WRITE(CLKCTRL.MCLKCTRLB, 0)"))

    def after_setup(self, f) -> None:
        f.add(cgen.Statement("sei()"))

    def cmake_name_add_library(self):
        return "add_avr_library"

    def cmake_name_target_include_directories(self):
        return "avr_target_include_directories"
