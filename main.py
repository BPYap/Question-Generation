import argparse
import subprocess

from qgen.util.config import load_yaml_config
from qgen.util.file import create_folder, get_filename

INPUT_FILENAME = ["build_parallel-src", "build_parallel-tgt"]
DATA_FILENAME = [
    "build_parallel-parallel_src",
    "build_parallel-parallel_tgt",

    "prepare_dataset-input_src",
    "prepare_dataset-input_tgt",
    "prepare_dataset-train_src",
    "prepare_dataset-train_tgt",
    "prepare_dataset-valid_src",
    "prepare_dataset-valid_tgt",
    "prepare_dataset-test_src",
    "prepare_dataset-test_tgt",

    "preprocess-train_src",
    "preprocess-train_tgt",
    "preprocess-valid_src",
    "preprocess-valid_tgt",
    "preprocess-save_data",

    "train-data",

    "translate-src",
    "translate-output",

    "format_output-src",
    "format_output-tgt",
    "format_output-output"
]
SAVE_MODEL_NAME = "train-save_model"
TRANSLATE_MODEL_NAME = "translate-model"
TRAIN_STEP = "train-train_steps"


def _process_file_path(experiment_name, config):
    # Convert file name of input files to relative path
    for input_file in INPUT_FILENAME:
        config[input_file] = config['corpus_directory'] + config[input_file]

    # Create new folder `<experiment_name>` in `data/output/` if not exist
    create_folder(f"data/output/{experiment_name}")

    # Convert file name of data files to relative path
    for data_file in DATA_FILENAME:
        config[data_file] = f"data/output/{experiment_name}/{config[data_file]}"

    # Convert file name of model file to relative path
    config[SAVE_MODEL_NAME] = f"model/{experiment_name}-{config[SAVE_MODEL_NAME]}"

    # Convert file name of saved model path to relative path
    config[TRANSLATE_MODEL_NAME] = f"{config[SAVE_MODEL_NAME]}_step_{config[TRAIN_STEP]}.pt"


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
    arguments = _filter_args(raw_configs, get_filename(script).split('.')[0])
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
    _process_file_path(get_filename(args.config).split('.')[0], configs)

    if args.script == 'all':
        for script_name, relative_path in valid_scripts.items():
            _run_python(relative_path, configs)
    else:
        _run_python(valid_scripts[args.script], configs)
