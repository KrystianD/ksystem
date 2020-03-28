from typing import List


def create_bitfield(names: List[str]):
    if len(names) == 0:
        return 0
    return " | ".join(f"_BV({x})" for x in names)
