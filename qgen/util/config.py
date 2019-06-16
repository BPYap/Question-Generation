import yaml


def load_yaml_config(path):
    with open(path, 'r') as stream:
        return yaml.safe_load(stream)
