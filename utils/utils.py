from typing import List, TypeVar, Type

import yaml


def create_bitfield_BV(names: List[str]):
    if len(names) == 0:
        return 0
    return " | ".join(f"_BV({x})" for x in names)


def create_bitfield_mask(names: List[str]):
    if len(names) == 0:
        return 0
    return " | ".join(f"{x}" for x in names)


def write_text_file(path, content):
    with open(path, "wt", encoding="utf-8") as f:
        f.write(content)


def read_yaml_file(path):
    with open(path, "rt") as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


T = TypeVar("T")


def load_config(path: str, cfg_type: Type[T]) -> T:
    config = cfg_type(**read_yaml_file(path))  # type: ignore
    return config
