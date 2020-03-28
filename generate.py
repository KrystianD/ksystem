import os

import cgen

from generator.SourceFile import SourceFile
from components.GPIO import GPIOComponent
from components.Serial import SerialComponent
from components.Systick import SysTickComponent
from config import load_config
from generator.StatementsContainer import StatementsContainer


def main():
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config', type=str, metavar="PATH", required=True)
    argparser.add_argument('-o', '--output-dir', type=str, metavar="PATH", required=True)

    args = argparser.parse_args()

    cfg = load_config(args.config)

    components = [
        SerialComponent(cfg),
        GPIOComponent(cfg),
        SysTickComponent(cfg),
    ]

    source_file = SourceFile()

    for component in components:
        for path in component.get_source_includes():
            if path is not None:
                source_file.add_include(path, True)

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

        loop_statements = StatementsContainer()
        loop_statements.add("loop()")

        for component in components:
            loop_statements.add_blank()
            loop_statements.add(cgen.LineComment(f"Component: {type(component).__name__}"))
            component.emit_loop(loop_statements)

        f.add(cgen.Statement("setup()"))
        f.add(cgen.For("", "", "", cgen.Block(loop_statements.statements)))

    source_file.save(os.path.join(args.output_dir, "ksystem.cpp"))

    header_file = SourceFile()

    for component in components:
        for path in component.get_header_includes():
            if path is not None:
                header_file.add_include(path, True)

    for component in components:
        header_file.add(cgen.LineComment(f"Component: {type(component).__name__}"))
        component.emit_extern_global_variables(header_file)
        header_file.add_blank()

    header_file.save(os.path.join(args.output_dir, "ksystem.h"))


if __name__ == "__main__":
    main()
