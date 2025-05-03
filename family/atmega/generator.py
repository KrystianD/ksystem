import os
from typing import Optional

import cgen

from common.Generator import BaseGenerator
from family.atmega.config import Config, SysTimerDef
from family.atmega.components.Modbus import ModbusComponent
from family.atmega.components.GPIO import GPIOComponent
from family.atmega.components.Serial import SerialComponent
from family.atmega.components.Systick import SysTickComponent

script_dir = os.path.dirname(os.path.realpath(__file__))


class AtmegaGenerator(BaseGenerator):
    def __init__(self, cfg: Config, output_dir: str):
        super().__init__(output_dir, script_dir)
        self.cfg = cfg

        self.add_global_define(f"F_CPU={self.cfg.frequency}")

    def prepare_components(self) -> None:
        serial: Optional[SerialComponent] = None
        systick: Optional[SysTickComponent] = None

        if self.cfg.components.serial is not None:
            serial = SerialComponent(self.cfg)
            self.add_component(serial)

        if self.cfg.components.systick is not None:
            systick = SysTickComponent(self.cfg)
            self.add_component(systick)

        if self.cfg.components.gpio is not None:
            gpio = GPIOComponent(self.cfg)
            self.add_component(gpio)

        if self.cfg.components.modbus is not None:
            assert systick is not None
            assert serial is not None

            modbus = ModbusComponent(self.cfg)
            systick.register_systimer(SysTimerDef(name="modbusTimer", repeat=False, handler=True, required_accuracy=1))
            self.add_component(modbus)

    def on_init(self, f) -> None:
        pass

    def after_setup(self, f) -> None:
        f.add(cgen.Statement("sei()"))

    def cmake_name_add_library(self):
        return "add_avr_library"

    def cmake_name_target_include_directories(self):
        return "avr_target_include_directories"
