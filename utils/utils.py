from typing import List


def create_bitfield(names: List[str]):
    if len(names) == 0:
        return 0
    return " | ".join(f"_BV({x})" for x in names)


def write_text_file(path, content):
    with open(path, "wt", encoding="utf-8") as f:
        f.write(content)
