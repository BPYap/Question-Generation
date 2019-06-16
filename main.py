import argparse
import subprocess

from qgen.util.config import load_yaml_config


def _filter_args(config, prefix):
    arguments = []

    for key in config:
        if key.startswith(prefix):
            arg_name = key[len(prefix):]
            value = config[key]
            if value not in ['false', 'none'] and (
                    not isinstance(value, list) or isinstance(value, list) and len(value) > 0):
                arguments.append('-' + arg_name)
                if value != 'true':
                    if isinstance(value, list):
                        value = " ".join([str(e) for e in value])
                    arguments.append(str(value))

    return arguments


def _run_python(script, arguments):
    command = ["python", script]
    command.extend(arguments)

    subprocess.run(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()

    configs = load_yaml_config(args.config)

    _run_python("script/build_parallel.py", _filter_args(configs, 'parallel'))
    _run_python("script/prepare_dataset.py", _filter_args(configs, 'prepare'))
    _run_python("OpenNMT-py/preprocess.py", _filter_args(configs, 'onmt-preprocess'))
    _run_python("OpenNMT-py/train.py", _filter_args(configs, 'onmt-train'))
    _run_python("OpenNMT-py/translate.py", _filter_args(configs, 'onmt-translate'))
