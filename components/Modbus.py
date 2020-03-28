from typing import List

import cgen

from components.component import IComponent
from generator.IStatementsContainer import IStatementsContainer
from hardware.timer2 import configure_timer2, Timer2Mode


class ModbusComponent(IComponent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.modbus = cfg.components.modbus

    def get_source_includes(self) -> List[str]:
        return [
        ]

    def get_header_includes(self) -> List[str]:
        return [
            "kModbus.h",
        ]

    def emit_extern_global_variables(self, source_file):
        source_file.add(cgen.Statement(f"static kModbus Modbus"))

        if self.modbus.rs485_dir_pin is not None:
            source_file.add(cgen.Define(f"MODBUS_RS485_DIR_PIN", self.modbus.rs485_dir_pin))

    def emit_global_variables(self, source_file):
        pass

    def emit_helper_functions(self, source_file):
        pass

    def emit_initialization(self, source_file):
        source_file.add(cgen.Statement("Modbus.init()"))

    def emit_loop(self, source_file: IStatementsContainer):
        source_file.add(cgen.Statement("Modbus.process()"))

    def get_additional_source_files(self) -> List[str]:
        return ["third-party/freemodbus/demo/AVR/port/portevent.c",
                "third-party/freemodbus/modbus/mb.c",
                "third-party/freemodbus/modbus/rtu/mbrtu.c",
                "third-party/freemodbus/modbus/functions/mbfunccoils.c",
                "third-party/freemodbus/modbus/functions/mbfuncdiag.c",
                "third-party/freemodbus/modbus/functions/mbfuncdisc.c",
                "third-party/freemodbus/modbus/functions/mbfuncholding.c",
                "third-party/freemodbus/modbus/functions/mbfuncinput.c",
                "third-party/freemodbus/modbus/functions/mbfuncother.c",
                "third-party/freemodbus/modbus/functions/mbutils.c",

                "third-party/freemodbus-avr-port/portserial.cpp",
                "third-party/freemodbus-avr-port/porttimer.cpp",
                "third-party/freemodbus-avr-port/mbcrc.c",

                "library/kModbus.cpp"]

    def get_additional_header_directories(self) -> List[str]:
        return ["third-party/freemodbus-avr-port/",
                "third-party/freemodbus/modbus/include/",
                "third-party/freemodbus/modbus/rtu/"]
