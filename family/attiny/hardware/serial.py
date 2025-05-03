import cgen as c

from family.attiny.components.GPIO import parse_port
from family.attiny.config import Config, SerialConfig
from family.attiny.devices import devices_variants
from utils.utils import create_bitfield_mask


def compare_pinout(serial_cfg: SerialConfig, pinout):
    pin_tx = serial_cfg.pin_tx
    pin_rx = serial_cfg.pin_rx

    if pin_tx is not None and pin_rx is not None:
        return pin_tx == pinout["pin_tx"] and pin_rx == pinout["pin_rx"]
    elif pin_tx is not None and pin_rx is None:
        return pin_tx == pinout["pin_tx"]
    elif pin_rx is not None and pin_tx is None:
        return pin_rx == pinout["pin_rx"]
    else:
        raise Exception("invalid")


def configure_serial(cfg: Config, serial_cfg: SerialConfig):
    stmts = []

    device_variant = devices_variants[cfg.device]
    baudrate = serial_cfg.baudrate

    usart_dev = serial_cfg.usart
    assert usart_dev in device_variant["usarts"]
    usart_dev_obj = device_variant["usarts"][usart_dev]

    # pinout
    pin_tx = serial_cfg.pin_tx
    pin_rx = serial_cfg.pin_rx
    pin_xdir = serial_cfg.pin_xdir

    pinout_cfg = [pinout for pinout in usart_dev_obj["pinout"]
                  if compare_pinout(serial_cfg, pinout)]
    assert len(pinout_cfg) == 1

    if pinout_cfg[0]["setup_code"] != "":
        stmts.append(c.Statement(pinout_cfg[0]["setup_code"]))

    if pin_tx is not None:
        portpin_tx = parse_port(pin_tx)
        stmts.append(c.Statement(f"{portpin_tx.to_kGPIO()} pinTx"))
        stmts.append(c.Statement(f"pinTx.pushPull()"))

    if pin_xdir is not None:
        portpin_xdir = parse_port(pin_xdir)
        stmts.append(c.Statement(f"{portpin_xdir.to_kGPIO()} pinXDir"))
        stmts.append(c.Statement(f"pinXDir.pushPull()"))
        stmts.append(c.Statement(f"pinXDir.low()"))

    # baud
    sel1 = round((cfg.frequency * 64) / (baudrate * 16))
    sel2 = round((cfg.frequency * 64) / (baudrate * 8))

    bd1 = (64 * cfg.frequency) / (16 * sel1)
    bd2 = (64 * cfg.frequency) / (8 * sel2)

    err1 = (bd1 / baudrate - 1) * 100
    err2 = (bd2 / baudrate - 1) * 100

    min_err = min(abs(err1), abs(err2))
    print(f"Serial error: {min_err}")
    if min_err >= 3:
        raise Exception("too big error")

    if abs(err1) <= abs(err2):
        use_sel = sel1
        use_double = False
    else:
        use_sel = sel2
        use_double = True

    # stmts.append(c.Statement(f'{usart_dev}.CTRLC = USART_CHSIZE_8BIT_gc;'))
    stmts.append(c.Statement(f'{usart_dev}.BAUD = {use_sel}'))

    CTRLA = []
    CTRLB = []

    if pin_tx is not None:
        CTRLB.append("USART_TXEN_bm")
    if pin_rx is not None:
        CTRLB.append("USART_RXEN_bm")
    if pin_xdir is not None:
        CTRLA.append("USART_RS485_bm")

    if use_double:
        CTRLB.append("USART_RXMODE_CLK2X_gc")

    stmts.append(c.Statement(f'{usart_dev}.CTRLA = {create_bitfield_mask(CTRLA)}'))
    stmts.append(c.Statement(f'{usart_dev}.CTRLB = {create_bitfield_mask(CTRLB)}'))

    return stmts
