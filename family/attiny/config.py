from dataclasses import field
from enum import Enum
from typing import Dict, Optional, List

from pydantic.dataclasses import dataclass


@dataclass
class SystickConfig:
    frequency: int


@dataclass
class SerialConfig:
    usart: str
    baudrate: int
    pin_tx: Optional[str] = None
    pin_rx: Optional[str] = None
    pin_xdir: Optional[str] = None


@dataclass
class StdioConfig:
    serial: str
    float: bool


class GPIOMode(Enum):
    Input = "input"
    PushPull = "push-pull"
    Analog = "analog"


class GPIOInterrupt(Enum):
    Disabled = "disabled"
    Both = "both"
    Low = "low"
    Rising = "rising"
    Falling = "falling"


@dataclass
class GPIOPinDef:
    port: str
    mode: GPIOMode
    value: bool = False
    interrupt: GPIOInterrupt = GPIOInterrupt.Disabled


@dataclass
class ModbusConfig:
    serial: str

    missing_as_zero: bool
    rs485_dir_pin: Optional[str] = None

    functions: List[str] = None


@dataclass
class Components:
    systick: Optional[SystickConfig] = None
    gpio: Optional[List[Dict[str, GPIOPinDef]]] = field(default_factory=list)
    serial: Optional[Dict[str, SerialConfig]] = None
    stdio: Optional[StdioConfig] = None
    modbus: Optional[ModbusConfig] = None


@dataclass
class Config:
    device: str
    frequency: int
    components: Components
