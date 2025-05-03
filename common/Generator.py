from abc import abstractmethod
from typing import List
import os

from common.component import IComponent
from generator.SourceFile import SourceFile
from generator.StatementsContainer import StatementsContainer
from utils.utils import write_text_file

import cgen


class BaseGenerator:
    def __init__(self, output_dir: str, script_dir: str):
        self.output_dir = output_dir
        self.script_dir = script_dir

        self._components: list[IComponent] = []
        self._defines: list[str] = []

    @abstractmethod
    def prepare_components(self) -> None: ...

    @abstractmethod
    def on_init(self, f) -> None: ...

    @abstractmethod
    def after_setup(self, f) -> None: ...

    @abstractmethod
    def cmake_name_add_library(self) -> str: ...

    @abstractmethod
    def cmake_name_target_include_directories(self) -> str: ...

    def add_global_define(self, define: str):
        self._defines.append(define)

    def add_component(self, component: IComponent):
        self._components.append(component)

    def build(self):
        ### SOURCE
        source_file = SourceFile(is_header=False)

        # source_file.add_include("stdint.h", True)

        for component in self._components:
            if not component.verify():
                exit(1)
            for src_path in component.get_source_includes():
                if src_path is not None:
                    source_file.add_include(src_path, True)

        source_file.add_include("ksystem.h", system=False)

        for component in self._components:
            component.emit_global_variables(source_file)

        source_file.add(cgen.Statement("extern void setup()"))
        source_file.add(cgen.Statement("extern void loop()"))
        source_file.add(cgen.Line())

        for component in self._components:
            source_file.add(cgen.LineComment(f"Component: {type(component).__name__}"))
            component.emit_helper_functions(source_file)
            source_file.add_blank()

        with source_file.function("int", "main") as f:
            self.on_init(f)

            for component in self._components:
                f.add(cgen.LineComment(f"Component: {type(component).__name__}"))
                component.emit_initialization(f)
                f.add_blank()

            f.add(cgen.Statement("setup()"))

            self.after_setup(f)

            loop_statements = StatementsContainer()
            loop_statements.add("loop()")

            for component in self._components:
                loop_statements.add_blank()
                loop_statements.add(cgen.LineComment(f"Component: {type(component).__name__}"))
                component.emit_loop(loop_statements)

            f.add(cgen.For("", "", "", cgen.Block(loop_statements.statements)))

        ksystem_cpp_path = os.path.join(self.output_dir, "ksystem.cpp")
        source_file.save(ksystem_cpp_path)

        ### HEADER
        header_file = SourceFile(is_header=True)

        for component in self._components:
            for header_path in component.get_header_includes():
                if header_path is not None:
                    header_file.add_include(header_path, True)

        for component in self._components:
            header_file.add(cgen.LineComment(f"Component: {type(component).__name__}"))
            component.emit_extern_global_variables(header_file)
            header_file.add_blank()

        header_file.save(os.path.join(self.output_dir, "ksystem.h"))

        ### INTERNAL HEADER
        internal_header_file = SourceFile(is_header=True)

        for component in self._components:
            internal_header_file.add(cgen.LineComment(f"Component: {type(component).__name__}"))
            component.emit_internal_header(internal_header_file)
            internal_header_file.add_blank()

        internal_header_file.save(os.path.join(self.output_dir, "ksystem_internal.h"))

        ### CMAKE
        sources = []
        include_dirs = []

        for component in self._components:
            sources += component.get_additional_source_files()
            include_dirs += component.get_additional_header_directories()

        output_dir_abs = os.path.abspath(self.output_dir)

        def get_path(path: str):
            path_abs = os.path.join(self.script_dir, path)
            return '${CMAKE_CURRENT_LIST_DIR}/' + os.path.relpath(path_abs, output_dir_abs)

        sources = [get_path(x) for x in sources]
        include_dirs = [get_path(x) for x in include_dirs]

        nl = "\n  "

        defines_str = " ".join(f"-D{x}" for x in self._defines)

        cmake_content = f"""
add_definitions({defines_str})

include_directories(${{CMAKE_CURRENT_LIST_DIR}})
include_directories({get_path("library")})

{self.cmake_name_add_library()}(ksystem STATIC
  ${{CMAKE_CURRENT_LIST_DIR}}/ksystem.cpp
  {nl.join(sources)}
)

{self.cmake_name_target_include_directories()}(ksystem PUBLIC
  {nl.join(include_dirs)}
)
""".lstrip()

        write_text_file(os.path.join(self.output_dir, "ksystem.cmake"), cmake_content)
