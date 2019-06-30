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
    valid_scripts = ['build_parallel', 'prepare_dataset', 'preprocess', 'train', 'translate', 'format', 'all']
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Configuration file (.yml) for all scripts")
    parser.add_argument("--script", "-s", default='all',
                        help="Choose to run an individual script. Available options: "
                             "{} (default: all)".format(valid_scripts))
    args = parser.parse_args()
    if args.script != 'all' and args.script not in valid_scripts:
        raise RuntimeError("Unknown script name: {}".format(args.script))

    configs = load_yaml_config(args.config)

    if args.script == 'all' or args.script == 'build_parallel':
        _run_python("script/build_parallel.py", _filter_args(configs, 'parallel'))

    if args.script == 'all' or args.script == 'prepare_dataset':
        _run_python("script/prepare_dataset.py", _filter_args(configs, 'prepare'))

    if args.script == 'all' or args.script == 'preprocess':
        _run_python("OpenNMT-py/preprocess.py", _filter_args(configs, 'onmt-preprocess'))

    if args.script == 'all' or args.script == 'train':
        _run_python("OpenNMT-py/train.py", _filter_args(configs, 'onmt-train'))

    if args.script == 'all' or args.script == 'translate':
        _run_python("OpenNMT-py/translate.py", _filter_args(configs, 'onmt-translate'))

    if args.script == 'all' or args.script == 'format':
        _run_python("script/format_output.py", _filter_args(configs, 'format'))
