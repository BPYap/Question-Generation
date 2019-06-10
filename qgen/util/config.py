import argparse
import yaml


def get_default_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config')

    return parser


def load_yaml_config():
    parser = get_default_argparser()
    args = parser.parse_args()

    if args.config is None:
        raise RuntimeError("--config is not specified")

    with open(args.config, 'r') as stream:
        return yaml.safe_load(stream)
