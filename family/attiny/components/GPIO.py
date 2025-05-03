from dataclasses import dataclass
from typing import List, Dict

import cgen

from common.component import IComponent
from family.attiny.components.Interrupts import InterruptsComponent
from family.attiny.config import GPIOPinDef, GPIOMode, GPIOInterrupt


@dataclass
class PortPin:
    port: str
    pin: int

    def to_kGPIO(self):
        return f"kGPIO<kPORT{self.port},{self.pin}>"


def parse_port(port_str: str) -> PortPin:
    port = port_str[0]
    assert port in ("A", "B", "C")
    pin = int(port_str[1])
    return PortPin(port, pin)


@dataclass
class GPIOInstance:
    name: str
    definition: GPIOPinDef
    portpin: PortPin

    @staticmethod
    def create(name: str, definition: GPIOPinDef):
        return GPIOInstance(name, definition, parse_port(definition.port))


class GPIOComponent(IComponent):
    def __init__(self, gpio_cfg: List[Dict[str, GPIOPinDef]], interrupts: InterruptsComponent):
        self.gpio_cfg = gpio_cfg
        self.interrupts = interrupts

        self.instances: List[GPIOInstance] = [GPIOInstance.create(list(x)[0], x[list(x)[0]]) for x in self.gpio_cfg]

        for instance in self.instances:
            pdef = instance.definition

            if pdef.interrupt != GPIOInterrupt.Disabled:
                interrupts.register_external_handler(
                    f"PORT{instance.portpin.port}_PORT",
                    f"{instance.name}_onInterrupt",
                    post_function=f"{instance.name}.clearInterruptFlag()")

    def get_source_includes(self) -> List[str]:
        return [
            "avr/io.h",
        ]

    def get_header_includes(self) -> List[str]:
        return [
            "kGPIO.h",
        ]

    def emit_extern_global_variables(self, source_file):
        for instance in self.instances:
            source_file.add(cgen.Statement(f"static {instance.portpin.to_kGPIO()} {instance.name}"))

    def emit_global_variables(self, source_file):
        pass

    def emit_helper_functions(self, source_file):
        pass

    def emit_initialization(self, source_file):
        for instance in self.instances:
            pdef = instance.definition

            # Mode
            if pdef.mode == GPIOMode.PushPull:
                source_file.add(cgen.Statement(f"{instance.name}.pushPull()"))
                if pdef.value is True:
                    source_file.add(cgen.Statement(f"{instance.name}.high()"))

            elif pdef.mode == GPIOMode.Analog:
                if pdef.interrupt != GPIOInterrupt.Disabled:
                    raise Exception("analog pin can't have interrupt enabled")

                source_file.add(cgen.Statement(f"{instance.name}.setMode(PORT_ISC_INPUT_DISABLE_gc)"))

            # Interrupts
            if pdef.interrupt != GPIOInterrupt.Disabled:
                if pdef.mode == GPIOMode.Analog:
                    raise Exception("analog pin can't have interrupt enabled")

                if pdef.interrupt == GPIOInterrupt.Low:
                    source_file.add(cgen.Statement(f"{instance.name}.setMode(PORT_ISC_LEVEL_gc)"))
                elif pdef.interrupt == GPIOInterrupt.Falling:
                    source_file.add(cgen.Statement(f"{instance.name}.setMode(PORT_ISC_FALLING_gc)"))
                elif pdef.interrupt == GPIOInterrupt.Rising:
                    source_file.add(cgen.Statement(f"{instance.name}.setMode(PORT_ISC_RISING_gc)"))
                elif pdef.interrupt == GPIOInterrupt.Both:
                    source_file.add(cgen.Statement(f"{instance.name}.setMode(PORT_ISC_BOTHEDGES_gc)"))
                else:
                    source_file.add(cgen.Statement(f"{instance.name}.setMode(PORT_ISC_INPUT_DISABLE_gc)"))

    def emit_loop(self, source_file):
        pass
