from dataclasses import field

import yaml
from typing import Dict, Optional, List

from pydantic import Field
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
    frequency: int
    components: Components


config: Optional[Config] = None


def load_config(path: str) -> Config:
    global config
    config = Config(**yaml.load(open(path, "rt"), Loader=yaml.SafeLoader))  # type: ignore
    return config


def get_config() -> Config:
    global config
    if config is None:
        raise Exception("no config")
    return config
