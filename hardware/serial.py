import cgen as c

from config import Config
from utils.utils import create_bitfield


def configure_serial(cfg: Config, baudrate: int):
    stmts = []

    sel1 = round(cfg.frequency / 16 / baudrate - 1)
    sel2 = round(cfg.frequency / 8 / baudrate - 1)

    bd1 = cfg.frequency / (16 * (sel1 + 1))
    bd2 = cfg.frequency / (8 * (sel2 + 1))

    err1 = (bd1 / baudrate - 1) * 100
    err2 = (bd2 / baudrate - 1) * 100

    min_err = min(abs(err1), abs(err2))
    if min_err >= 3:
        raise Exception("too big error")

    if abs(err1) <= abs(err2):
        use_sel = sel1
        use_double = False
    else:
        use_sel = sel2
        use_double = True

    stmts.append(c.Statement(f'const uint16_t UBRR = {use_sel}'))
    stmts.append(c.Statement(f'UBRRH = (uint8_t)(UBRR >> 8u) & 0xffu'))
    stmts.append(c.Statement(f'UBRRL = (uint8_t)(UBRR >> 0u) & 0xffu'))

    UCSRA = []

    if use_double:
        UCSRA.append("U2X")

    stmts.append(c.Statement(f'UCSRA = {create_bitfield(UCSRA)}'))

    UCSRB = ["RXEN", "TXEN"]
    stmts.append(c.Statement(f'UCSRB = {create_bitfield(UCSRB)}'))

    UCSRC = ["URSEL"]

    UCSRC += ["UCSZ1", "UCSZ0"]  # 8-bit

    stmts.append(c.Statement(f'UCSRC = {create_bitfield(UCSRC)}'))

    return stmts
