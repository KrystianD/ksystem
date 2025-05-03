from typing import List

import cgen

from common.component import IComponent
from family.attiny.components.Interrupts import InterruptsComponent
from family.attiny.config import Config
from generator.IStatementsContainer import IStatementsContainer
from generator.SourceFile import SourceFile


class SysTickComponent(IComponent):
    def __init__(self, cfg: Config, interrupts: InterruptsComponent):
        self.cfg = cfg

        interrupts.register_handler("RTC_CNT", "SysTick.handleInterrupt()")

    def get_source_includes(self) -> List[str]:
        return [
        ]

    def get_header_includes(self) -> List[str]:
        return [
            "kSysTick.h",
        ]

    def verify(self):
        return True

    def emit_extern_global_variables(self, source_file):
        oscillator_tick = 1 / 32768
        period_ms = 1 / self.cfg.components.systick.frequency
        period = round(period_ms / oscillator_tick)

        s = period * oscillator_tick
        print("Actual systick frequency:", 1 / s)

        source_file.add(cgen.Statement(f"typedef kSysTick<{period}> kConfiguredSysTick"))
        source_file.add(cgen.Statement(f"extern kConfiguredSysTick SysTick"))

    def emit_global_variables(self, source_file):
        source_file.add(cgen.Statement(f"kConfiguredSysTick SysTick"))

    def emit_helper_functions(self, source_file: SourceFile):
        pass

    def emit_initialization(self, source_file):
        source_file.add(cgen.Statement("SysTick.init()"))

    def emit_loop(self, source_file: IStatementsContainer):
        pass
