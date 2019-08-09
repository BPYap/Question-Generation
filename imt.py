import argparse
import subprocess

from tqdm import tqdm

import qgen.util.file as file_util
from qgen.corpusbuilder.builder import Builder
from qgen.encoder.fasttext import FTEncoder
from qgen.encoder.glove import GloveEncoder
from qgen.encoder.universal_sentence_encoder import USEEncoder
from qgen.util.config import load_yaml_config

PARALLEL_SOURCE = 'parallel_source.txt'
PARALLEL_TARGET = 'parallel_tgt.txt'
RESULT_JSON = 'result.json'

FILE_ARGS = {
    'prepare_dataset-input_src': PARALLEL_SOURCE,
    'prepare_dataset-input_tgt': PARALLEL_TARGET,
    'prepare_dataset-train_src': 'train_source.txt',
    'prepare_dataset-train_tgt': 'train_target.txt',
    'prepare_dataset-valid_src': 'validation_source.txt',
    'prepare_dataset-valid_tgt': 'validation_target.txt',
    'prepare_dataset-test_src': 'test_source.txt',
    'prepare_dataset-test_tgt': 'test_target.txt',

    'preprocess-train_src': 'train_source.txt',
    'preprocess-train_tgt': 'train_target.txt',
    'preprocess-valid_src': 'validation_source.txt',
    'preprocess-valid_tgt': 'validation_target.txt',
    'preprocess-save_data': 'onmt_data',

    'train-data': 'onmt_data',

    'translate-src': PARALLEL_SOURCE,  # 'test_source.txt'
    'translate-output': 'predicted_target.txt',

    'format_output-src': PARALLEL_SOURCE,  # 'test_source.txt'
    'format_output-tgt': 'predicted_target.txt',
    'format_output-output': RESULT_JSON
}


def _process_data_path(sub_data_dir, yaml_config):
    # Convert file name of data files to relative path
    for arg_name, file_name in FILE_ARGS.items():
        yaml_config[arg_name] = f"{sub_data_dir}/{file_name}"


def _process_model_path(model_dir, iteration, yaml_config):
    # Add `train-save_model`
    model_name = f"{model_dir}/{iteration}-onmt_model"
    yaml_config["train-save_model"] = model_name

    # Add `translate-model`
    yaml_config['translate-model'] = f"{model_name}_step_{yaml_config['train-train_steps']}.pt"


def _filter_args(yaml_config, prefix):
    arguments = []

    for key in yaml_config:
        if key.startswith(prefix):
            arg_name = key[len(prefix):]
            value = yaml_config[key]

            if value not in ['false', 'none'] and (
                    not isinstance(value, list) or isinstance(value, list) and len(value) > 0):
                arguments.append('-' + arg_name)
                if value != 'true':
                    if isinstance(value, list):
                        value = " ".join([str(e) for e in value])
                    arguments.append(str(value))

    return arguments


def _run_python_script(script, yaml_config):
    command = ["python", script]
    arguments = _filter_args(yaml_config, file_util.get_filename(script).split('.')[0])
    command.extend(arguments)

    subprocess.run(command)


def _init_builder(tgt_path, encoder):
    pretrained_config = load_yaml_config("config/pretrained.yml")
    fasttext_path = pretrained_config['fasttext_model_path']
    glove_path = pretrained_config['glove_model_path']
    use_path = pretrained_config['use_model_path']

    builder = Builder(tgt_path)

    if encoder == 'fasttext':
        builder.set_encoder(FTEncoder(fasttext_path))
    elif encoder == 'glove':
        builder.set_encoder(GloveEncoder(glove_path))
    else:
        builder.set_encoder(USEEncoder(use_path))

    return builder


def _bootstrap_parallel(builder, src_path, threshold, src_output_path, tgt_output_path):
    print("Bootstrapping pseudo-parallel corpus...")
    pseudo_parallel_corpus = dict()
    for src_sentence in tqdm(file_util.read_file(src_path)):
        if src_sentence in pseudo_parallel_corpus:
            continue

        most_similar_sentence = builder.get_most_similar_target(src_sentence, threshold)
        if most_similar_sentence is not None:
            pseudo_parallel_corpus[src_sentence] = most_similar_sentence

    file_util.write_file(pseudo_parallel_corpus.keys(), src_output_path)
    file_util.write_file(pseudo_parallel_corpus.values(), tgt_output_path)


def _refine_parallel(builder, src_parallel_path, tgt_parallel_path, candidate_path, src_output_path, tgt_output_path):
    print("Refinining pseudo-parallel corpus...")
    src_sentences = file_util.read_file(src_parallel_path)
    tgt_sentences = file_util.read_file(tgt_parallel_path)

    candidates = file_util.read_json(candidate_path)
    pseudo_parallel_corpus = {src_sentences[i]: tgt_sentences[i] for i in range(len(src_sentences))}
    refined_count = 0
    for src_sentence, current_target in tqdm(pseudo_parallel_corpus.items()):
        candidate = candidates[src_sentence][0]
        refined_target = builder.get_refined_target(src_sentence, current_target, candidate)

        if pseudo_parallel_corpus[src_sentence] != refined_target:
            refined_count += 1
            pseudo_parallel_corpus[src_sentence] = refined_target

    file_util.write_file(pseudo_parallel_corpus.keys(), src_output_path)
    file_util.write_file(pseudo_parallel_corpus.values(), tgt_output_path)

    update_rate = refined_count / len(pseudo_parallel_corpus)
    print(f"Number of pairs refined: {refined_count} ({update_rate * 100}%)")

    return update_rate


def main(config_path):
    experiment_name = file_util.get_filename(config_path).split('.')[0]
    yaml_config = load_yaml_config(config_path)

    # Extract general configurations
    src_corpus = yaml_config['src_corpus']
    tgt_corpus = yaml_config['tgt_corpus']
    min_update_rate = yaml_config['min_update_rate']
    sentence_encoder = yaml_config['bootstrap_corpus-sentence_encoder']
    similarity_threshold = yaml_config['bootstrap_corpus-similarity_threshold']

    # Path to other scripts
    prepare_dataset = 'script/utility/prepare_dataset.py'
    preprocess = 'OpenNMT-py/preprocess.py'
    train = 'OpenNMT-py/train.py'
    translate = 'OpenNMT-py/translate.py'
    format_output = 'script/utility/format_output.py'

    # Create new folder `<experiment_name>` under `data/output/`
    data_dir = f"data/output/{experiment_name}"
    file_util.create_folder(data_dir)

    # Create new folder `<experiment_name>` under `model/`
    model_dir = f"model/{experiment_name}"
    file_util.create_folder(model_dir)

    builder = _init_builder(tgt_corpus, sentence_encoder)
    current_iteration = 0
    while True:
        print(f"Current iteration: {current_iteration}")
        # Create sub-folder `<current_iteration>` under `data_dir`
        prev_sub_data_dir = f"{data_dir}/{current_iteration - 1}"
        sub_data_dir = f"{data_dir}/{current_iteration}"
        file_util.create_folder(sub_data_dir)

        _process_data_path(sub_data_dir, yaml_config)
        _process_model_path(model_dir, current_iteration, yaml_config)

        if current_iteration == 0:
            # Bootstrap pseudo-parallel corpus
            source_output_path = f"{sub_data_dir}/{PARALLEL_SOURCE}"
            target_output_path = f"{sub_data_dir}/{PARALLEL_TARGET}"
            _bootstrap_parallel(builder, src_corpus, similarity_threshold, source_output_path, target_output_path)
        else:
            # Refine pseudo-parallel corpus
            source_parallel_path = f"{prev_sub_data_dir}/{PARALLEL_SOURCE}"
            target_parallel_path = f"{prev_sub_data_dir}/{PARALLEL_TARGET}"
            candidate_json_path = f"{prev_sub_data_dir}/{RESULT_JSON}"
            source_output_path = f"{sub_data_dir}/{PARALLEL_SOURCE}"
            target_output_path = f"{sub_data_dir}/{PARALLEL_TARGET}"

            update_rate = _refine_parallel(builder, source_parallel_path, target_parallel_path, candidate_json_path,
                                           source_output_path, target_output_path)

            if update_rate < min_update_rate:
                # Terminate if update rate is less than the specified value
                print("Done.")
                exit(1)

        print("Splitting data set...")
        _run_python_script(prepare_dataset, yaml_config)

        print("Pre-processing data set...")
        _run_python_script(preprocess, yaml_config)

        print("Training neural machine translation model...")
        _run_python_script(train, yaml_config)

        print("Translating...")
        _run_python_script(translate, yaml_config)

        print("Formatting output...")
        _run_python_script(format_output, yaml_config)

        current_iteration += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Configuration file (.yml) for all scripts")
    args = parser.parse_args()

    main(args.config)