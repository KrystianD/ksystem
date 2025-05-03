from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict

import cgen

from common.component import IComponent
from generator.SourceFile import SourceFile


@dataclass
class InterruptHandler:
    is_extern: bool
    function_name: str
    body_lines: List[str]


class InterruptsComponent(IComponent):
    def __init__(self):
        self.signals: Dict[str, List[InterruptHandler]] = defaultdict(list)

    def register_external_handler(self, signal_name: str, function_name: str, post_function: str):
        self.signals[signal_name].append(InterruptHandler(True, function_name, body_lines=[
            f"{function_name}()",
            post_function]))

    def register_handler(self, signal_name: str, body: str):
        self.signals[signal_name].append(InterruptHandler(False, "", [body]))

    def get_source_includes(self) -> List[str]:
        return []

    def get_header_includes(self) -> List[str]:
        return []

    def emit_extern_global_variables(self, source_file: SourceFile):
        for signal_name, functions in self.signals.items():
            for function in functions:
                if function.is_extern:
                    source_file.add(cgen.Statement(f"extern void {function.function_name}()"))

    def emit_global_variables(self, source_file: SourceFile):
        for signal_name, functions in self.signals.items():
            source_file.add(cgen.Line(f"""ISR({signal_name}_vect)"""))
            bl = cgen.Block()

            for function in functions:
                for line in function.body_lines:
                    bl.append(cgen.Statement(line))
            source_file.add(bl)

    def emit_helper_functions(self, source_file: SourceFile):
        pass

    def emit_initialization(self, source_file: SourceFile):
        pass

    def emit_loop(self, source_file):
        pass
