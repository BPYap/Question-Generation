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


def _run_python(script, raw_configs):
    command = ["python", script]
    arguments = _filter_args(raw_configs, script.split('/')[-1].split('.')[0])
    command.extend(arguments)

    subprocess.run(command)


if __name__ == '__main__':
    # {<script_name>: <relative_path}
    valid_scripts = {
        'build_parallel': 'script/build_parallel.py',
        'prepare_dataset': 'script/prepare_dataset.py',
        'preprocess': 'OpenNMT-py/preprocess.py',
        'train': 'OpenNMT-py/train.py',
        'translate': 'OpenNMT-py/translate.py',
        'format_output': 'script/format_output.py'
    }
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Configuration file (.yml) for all scripts")
    parser.add_argument("--script", "-s", default='all',
                        help="Choose to run an individual script. Available options: "
                             f"[{', '.join(valid_scripts.keys())}]")
    args = parser.parse_args()
    if args.script != 'all' and args.script not in valid_scripts:
        print(f"Unknown script '{args.script}'. Available options: [{', '.join(valid_scripts.keys())}]")
        exit(-1)

    configs = load_yaml_config(args.config)

    if args.script == 'all':
        for script_name, relative_path in valid_scripts.items():
            _run_python(relative_path, configs)
    else:
        _run_python(valid_scripts[args.script], configs)
