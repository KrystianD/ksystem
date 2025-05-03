from dataclasses import field

import yaml
from typing import Dict, Optional, List

from pydantic import Field, Extra
from pydantic.dataclasses import dataclass


@dataclass
class SysTimerDef:
    name: str
    repeat: bool
    handler: bool
    required_accuracy: float = None


@dataclass
class Systick:
    frequency: int
    timer: int
    systimers: List[SysTimerDef] = field(default_factory=list)


@dataclass
class Serial:
    baudrate: int
    stdio: bool = False


@dataclass
class GPIOPinDef:
    port: str
    mode: str
    value: bool = False


@dataclass
class Modbus:
    missing_as_zero: bool
    rs485_dir_pin: Optional[str] = None

    functions: List[str] = None


@dataclass
class Components:
    systick: Optional[Systick] = None
    gpio: Optional[List[Dict[str, GPIOPinDef]]] = field(default_factory=list)
    serial: Optional[Serial] = None
    modbus: Optional[Modbus] = None


@dataclass
class Config:
    family: str
    frequency: int
    components: Components
