from dataclasses import dataclass
from typing import List

import cgen

from components.component import IComponent
from generator.IStatementsContainer import IStatementsContainer
from generator.SourceFile import SourceFile
from hardware.timer2 import configure_timer2, Timer2Mode


@dataclass
class SysTimerDef:
    name: str
    restarting: bool


class SysTickComponent(IComponent):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.systick = self.cfg.components.systick

        f_cpu = self.cfg.frequency

        systick_prescaler = 256
        systick_count = f_cpu // self.cfg.components.systick.frequency // systick_prescaler
        systick_real_interval = f_cpu // systick_count // systick_prescaler

        systick_error = (systick_real_interval / self.cfg.components.systick.frequency - 1) * 100
        assert systick_error == 0

        self.systick_overflows = systick_count // 256
        self.systick_remainder = systick_count - self.systick_overflows * 256

        assert self.systick_overflows < 256

        self.systimers: List[SysTimerDef] = []

    def register_systimer(self, name: str, restarting: bool):
        self.systimers.append(SysTimerDef(name, restarting))

    def get_source_includes(self) -> List[str]:
        return [
        ]

    def get_header_includes(self) -> List[str]:
        return [
            "kSysTick.h",
            "kSysTimer.h",
        ]

    def emit_extern_global_variables(self, source_file):
        systick_interval = int(1000 / self.systick.frequency)

        source_file.add(cgen.Statement(f"using kConfiguredSysTick = kSysTick<{self.systick_overflows},{self.systick_remainder}>"))
        source_file.add(cgen.Statement(f"static kConfiguredSysTick SysTick"))

        for systimer in self.systimers:
            source_file.add(cgen.Statement(f"extern void {systimer.name}Elapsed()"))
            source_file.add(cgen.Statement(f"extern kSysTimer<{systick_interval},{systimer.name}Elapsed,{'true' if systimer.restarting else 'false'}> {systimer.name}"))

    def emit_global_variables(self, source_file):
        systick_interval = int(1000 / self.systick.frequency)

        source_file.add(cgen.Statement(f"template<> volatile uint8_t kConfiguredSysTick::_overflowCounter = 0"))
        source_file.add(cgen.Statement(f"template<> volatile uint8_t kConfiguredSysTick::_nextStep = 0"))
        source_file.add(cgen.Statement(f"template<> volatile uint16_t kConfiguredSysTick::_ticks = 0"))
        source_file.add(cgen.Line())

        for systimer in self.systimers:
            source_file.add(cgen.Statement(f"kSysTimer<{systick_interval},{systimer.name}Elapsed,{'true' if systimer.restarting else 'false'}> {systimer.name}"))

    def emit_helper_functions(self, source_file: SourceFile):
        source_file.add(cgen.Line("""SIGNAL(TIMER2_COMP_vect)"""))
        source_file.add(cgen.Block([cgen.Statement("SysTick.handleInterrupt()")]))

        with source_file.function("void", "kSysTickElapsed") as f:
            for systimer in self.systimers:
                f.add(cgen.Statement(f"{systimer.name}.handleTick()"))

    def emit_initialization(self, source_file):
        source_file.add(configure_timer2(Timer2Mode.CTC, prescaler=256,
                                         initial_value=0, compare_value=255,
                                         interrupt_match_enabled=True, interrupt_overflow_enabled=False))

        source_file.add(cgen.Statement("SysTick.init()"))

    def emit_loop(self, source_file: IStatementsContainer):
        for systimer in self.systimers:
            source_file.add(cgen.Statement(f"{systimer.name}.process()"))
