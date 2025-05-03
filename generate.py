import os

from utils.utils import read_yaml_file, load_config

script_dir = os.path.dirname(os.path.realpath(__file__))


def main():
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-c', '--config', type=str, metavar="PATH", required=True)
    argparser.add_argument('-o', '--output-dir', type=str, metavar="PATH", required=True)

    args = argparser.parse_args()

    cfg = read_yaml_file(args.config)

    if cfg["family"] == "atmega":
        from family.atmega.config import Config
        from family.atmega.generator import AtmegaGenerator
        AtmegaGenerator(load_config(args.config, Config), args.output_dir).build()
    elif cfg["family"] == "attiny":
        from family.attiny.config import Config
        from family.attiny.generator import AttinyGenerator
        AttinyGenerator(load_config(args.config, Config), args.output_dir).build()
    else:
        print("invalid family")
        exit(1)

if __name__ == "__main__":
    main()
