import os
from typing import Optional

import cgen

from components.Modbus import ModbusComponent
from generator.SourceFile import SourceFile
from components.GPIO import GPIOComponent
from components.Serial import SerialComponent
from components.Systick import SysTickComponent
from config import load_config, SysTimerDef
from generator.StatementsContainer import StatementsContainer
from utils.utils import write_text_file

script_dir = os.path.dirname(os.path.realpath(__file__))


def main():
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config', type=str, metavar="PATH", required=True)
    argparser.add_argument('-o', '--output-dir', type=str, metavar="PATH", required=True)

    args = argparser.parse_args()

    cfg = load_config(args.config)

    components = []

    serial: Optional[SerialComponent] = None
    systick: Optional[SysTickComponent] = None

    if cfg.components.serial is not None:
        serial = SerialComponent(cfg)
        components.append(serial)

    if cfg.components.systick is not None:
        systick = SysTickComponent(cfg)
        components.append(systick)

    if cfg.components.gpio is not None:
        gpio = GPIOComponent(cfg)
        components.append(gpio)

    if cfg.components.modbus is not None:
        assert systick is not None
        assert serial is not None

        modbus = ModbusComponent(cfg)
        systick.register_systimer(SysTimerDef(name="modbusTimer", repeat=False, handler=True, required_accuracy=1))
        components.append(modbus)

    ### SOURCE
    source_file = SourceFile(is_header=False)

    # source_file.add_include("stdint.h", True)

    for component in components:
        if not component.verify():
            exit(1)
        for src_path in component.get_source_includes():
            if src_path is not None:
                source_file.add_include(src_path, True)

    source_file.add_include("ksystem.h", system=False)

    for component in components:
        component.emit_global_variables(source_file)

    source_file.add(cgen.Statement("extern void setup()"))
    source_file.add(cgen.Statement("extern void loop()"))
    source_file.add(cgen.Line())

    for component in components:
        source_file.add(cgen.LineComment(f"Component: {type(component).__name__}"))
        component.emit_helper_functions(source_file)
        source_file.add_blank()

    with source_file.function("int", "main") as f:

        for component in components:
            f.add(cgen.LineComment(f"Component: {type(component).__name__}"))
            component.emit_initialization(f)
            f.add_blank()

        f.add(cgen.Statement("setup()"))

        f.add(cgen.Statement("sei()"))

        loop_statements = StatementsContainer()
        loop_statements.add("loop()")

        for component in components:
            loop_statements.add_blank()
            loop_statements.add(cgen.LineComment(f"Component: {type(component).__name__}"))
            component.emit_loop(loop_statements)

        f.add(cgen.For("", "", "", cgen.Block(loop_statements.statements)))

    ksystem_cpp_path = os.path.join(args.output_dir, "ksystem.cpp")
    source_file.save(ksystem_cpp_path)

    ### HEADER
    header_file = SourceFile(is_header=True)

    for component in components:
        for header_path in component.get_header_includes():
            if header_path is not None:
                header_file.add_include(header_path, True)

    for component in components:
        header_file.add(cgen.LineComment(f"Component: {type(component).__name__}"))
        component.emit_extern_global_variables(header_file)
        header_file.add_blank()

    header_file.save(os.path.join(args.output_dir, "ksystem.h"))

    ### INTERNAL HEADER
    internal_header_file = SourceFile(is_header=True)

    for component in components:
        internal_header_file.add(cgen.LineComment(f"Component: {type(component).__name__}"))
        component.emit_internal_header(internal_header_file)
        internal_header_file.add_blank()

    internal_header_file.save(os.path.join(args.output_dir, "ksystem_internal.h"))

    ### CMAKE
    sources = []
    include_dirs = []

    for component in components:
        sources += component.get_additional_source_files()
        include_dirs += component.get_additional_header_directories()

    output_dir_abs = os.path.abspath(args.output_dir)

    def get_path(path: str):
        path_abs = os.path.join(script_dir, path)
        return '${CMAKE_CURRENT_LIST_DIR}/' + os.path.relpath(path_abs, output_dir_abs)

    sources = [get_path(x) for x in sources]
    include_dirs = [get_path(x) for x in include_dirs]

    nl = "\n  "

    cmake_content = f"""
add_definitions(-DF_CPU={cfg.frequency})

include_directories(${{CMAKE_CURRENT_LIST_DIR}})
include_directories({get_path("library")})

add_avr_library(ksystem STATIC
  ${{CMAKE_CURRENT_LIST_DIR}}/ksystem.cpp
  {nl.join(sources)}
)

avr_target_include_directories(ksystem PUBLIC
  {nl.join(include_dirs)}
)
""".lstrip()

    write_text_file(os.path.join(args.output_dir, "ksystem.cmake"), cmake_content)


if __name__ == "__main__":
    main()
