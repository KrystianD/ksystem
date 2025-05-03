from enum import Enum
import cgen as c

from utils.utils import create_bitfield


class Timer2Mode(Enum):
    Normal = 0
    PWM_PhaseCorrect = 1
    CTC = 2
    FastPWM = 3


timer2_prescalers = [0, 1, 8, 32, 64, 128, 256, 1024]


def configure_timer2(mode: Timer2Mode, prescaler: int,
                     initial_value: int = None, compare_value: int = None,
                     interrupt_overflow_enabled=False,
                     interrupt_match_enabled=False):
    assert prescaler in timer2_prescalers
    assert 0 <= initial_value <= 255
    assert 0 <= compare_value <= 255

    TCCR2 = []

    if mode == Timer2Mode.Normal:
        TCCR2 += []
    elif mode == Timer2Mode.PWM_PhaseCorrect:
        TCCR2 += ["WGM20"]
    elif mode == Timer2Mode.CTC:
        TCCR2 += ["WGM21"]
    elif mode == Timer2Mode.FastPWM:
        TCCR2 += ["WGM21", "WGM20"]

    if prescaler == 0:
        pass
    elif prescaler == 1:
        TCCR2 += ["CS20"]
    elif prescaler == 8:
        TCCR2 += ["CS21"]
    elif prescaler == 32:
        TCCR2 += ["CS21", "CS20"]
    elif prescaler == 64:
        TCCR2 += ["CS22"]
    elif prescaler == 128:
        TCCR2 += ["CS22", "CS20"]
    elif prescaler == 256:
        TCCR2 += ["CS22", "CS21"]
    elif prescaler == 1024:
        TCCR2 += ["CS22", "CS21", "CS20"]

    stmts = []

    if initial_value is not None:
        stmts.append(c.Statement(f'TCNT2 = {initial_value}'))
    if compare_value is not None:
        stmts.append(c.Statement(f'OCR2 = {compare_value}'))

    stmts.append(c.Statement(f'TCCR2 = {create_bitfield(TCCR2)}'))

    TIMSK = []

    if interrupt_match_enabled is True:
        TIMSK.append("OCIE2")
    if interrupt_overflow_enabled is True:
        TIMSK.append("TOIE2")

    if compare_value is not None:
        stmts.append(c.Statement(f'TIMSK = {create_bitfield(TIMSK)}'))

    return stmts
