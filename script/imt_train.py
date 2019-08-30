import argparse
import math
import os
import subprocess
import threading

from tqdm.auto import tqdm

import qgen.util.file as file_util
import qgen.util.nlp as nlp_util
from qgen.corpus import Corpus
from qgen.encoder.fasttext import FTEncoder
from qgen.encoder.glove import GloveEncoder
from qgen.encoder.universal_sentence_encoder import USEEncoder
from qgen.util.config import load_yaml_config

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PRETRAINED_CONFIG_PATH = os.path.join(ROOT_PATH, "config/pretrained/encoder.yml")

PREPARE_DATASET_SCRIPT = os.path.join(ROOT_PATH, 'script/utility/prepare_dataset.py')
PREPROCESS_SCRIPT = os.path.join(ROOT_PATH, 'OpenNMT-py/preprocess.py')
TRAIN_SCRIPT = os.path.join(ROOT_PATH, 'OpenNMT-py/train.py')
TRANSLATE_SCRIPT = os.path.join(ROOT_PATH, 'OpenNMT-py/translate.py')
FORMAT_OUTPUT_SCRIPT = os.path.join(ROOT_PATH, 'script/utility/format_output.py')

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


def _resolve_data_path(yaml_config, sub_data_dir):
    # Convert file name of data files to relative path
    for arg_name, file_name in FILE_ARGS.items():
        yaml_config[arg_name] = f"{sub_data_dir}/{file_name}"


def _resolve_model_path(yaml_config, model_dir, iteration):
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


def _init_corpus(target_path, annoy_index_path, encoder_name):
    pretrained_config = load_yaml_config(PRETRAINED_CONFIG_PATH)
    fasttext_path = os.path.join(ROOT_PATH, pretrained_config['fasttext_model_path'])
    glove_path = os.path.join(ROOT_PATH, pretrained_config['glove_model_path'])
    use_path = os.path.join(ROOT_PATH, pretrained_config['use_model_path'])

    if encoder_name == 'fasttext':
        encoder = FTEncoder(fasttext_path)
    elif encoder_name == 'glove':
        encoder = GloveEncoder(glove_path)
    else:
        encoder = USEEncoder(use_path)

    return Corpus(target_path, annoy_index_path, encoder)


def _bootstrap_parallel(corpus, src_path, threshold, src_output_path, tgt_output_path):
    print("Bootstrapping pseudo-parallel corpus...")
    source_sentences = file_util.read_file(src_path, unique=True)

    progress_bar = tqdm(total=len(source_sentences))
    thread_lock = threading.Lock()

    def run_thread(corpus_, threshold_, batch_, update_dict):
        nonlocal progress_bar
        for source_sentence in batch_:
            most_similar_sentence = corpus_.get_most_similar_sentence(source_sentence, threshold_)

            if most_similar_sentence is not None:
                update_dict[source_sentence] = most_similar_sentence

            with thread_lock:
                progress_bar.update()

    pseudo_parallel_corpus = dict()
    threads = list()
    num_threads = 5
    batch_size = math.ceil(len(source_sentences) / num_threads)
    for i in range(0, len(source_sentences), batch_size):
        batch = source_sentences[i:i + batch_size]
        thread = threading.Thread(target=run_thread,
                                  args=(corpus, threshold, batch, pseudo_parallel_corpus))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    progress_bar.close()

    file_util.write_file(list(pseudo_parallel_corpus.keys()), src_output_path)
    file_util.write_file(list(pseudo_parallel_corpus.values()), tgt_output_path)


def _refine_parallel(corpus, src_parallel_path, tgt_parallel_path, candidate_path, src_output_path, tgt_output_path):
    print("Refinining pseudo-parallel corpus...")

    def get_refined_target(src, current_tgt, candidate_tgt):
        """ Refine a pair of pseudo-parallel sentences.
        """
        current_wmd = nlp_util.get_word_mover_dist(src, current_tgt)
        candidate_wmd = nlp_util.get_word_mover_dist(src, candidate_tgt)

        new_target, new_target_wmd = (current_tgt, current_wmd) if current_wmd < candidate_wmd \
            else (candidate_tgt, candidate_wmd)

        most_similar_original = corpus.get_most_similar_sentence(new_target, threshold=0)
        original_wmd = nlp_util.get_word_mover_dist(src, most_similar_original)

        return new_target if new_target_wmd < original_wmd else most_similar_original

    src_sentences = file_util.read_file(src_parallel_path)
    tgt_sentences = file_util.read_file(tgt_parallel_path)

    candidates = file_util.read_json(candidate_path)
    pseudo_parallel_corpus = {src_sentences[i]: tgt_sentences[i] for i in range(len(src_sentences))}

    progress_bar = tqdm(total=len(src_sentences))
    refined_count = 0
    thread_lock = threading.Lock()

    def run_thread(src_batch_, tgt_batch_):
        nonlocal progress_bar
        nonlocal refined_count

        for j in range(len(src_batch_)):
            source_sentence = src_batch_[j]
            current_target = tgt_batch_[j]

            candidate = candidates[source_sentence][0]
            refined_target = get_refined_target(source_sentence, current_target, candidate)

            if pseudo_parallel_corpus[source_sentence] != refined_target:
                with thread_lock:
                    refined_count += 1

                pseudo_parallel_corpus[source_sentence] = refined_target

            with thread_lock:
                progress_bar.update()

    threads = list()
    num_threads = 5
    batch_size = math.ceil(len(src_sentences) / num_threads)
    for i in range(0, len(src_sentences), batch_size):
        src_batch = src_sentences[i:i + batch_size]
        tgt_batch = tgt_sentences[i:i + batch_size]

        thread = threading.Thread(target=run_thread,
                                  args=(src_batch, tgt_batch))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    progress_bar.close()

    file_util.write_file(pseudo_parallel_corpus.keys(), src_output_path)
    file_util.write_file(pseudo_parallel_corpus.values(), tgt_output_path)

    update_rate = refined_count / len(pseudo_parallel_corpus)
    print(f"Number of pairs refined: {refined_count} ({update_rate * 100}%)")

    return update_rate


def main(config_path, starting_iteration=0):
    experiment_name = file_util.get_filename(config_path).split('.')[0]
    yaml_config = load_yaml_config(config_path)

    # Extract general configurations
    src_corpus = yaml_config['src_corpus']
    tgt_corpus = yaml_config['tgt_corpus']
    min_update_rate = yaml_config['min_update_rate']
    sentence_encoder = yaml_config['bootstrap_corpus-sentence_encoder']
    similarity_threshold = yaml_config['bootstrap_corpus-similarity_threshold']

    # Set the `num_sent` argument for `format_output.py`
    yaml_config['format_output-num_sent'] = yaml_config['translate-n_best']

    # Create new folder `<experiment_name>` under `data/output/`
    data_dir = os.path.join(ROOT_PATH, f"data/imt/{experiment_name}")
    file_util.create_folder(data_dir)

    # Create new folder `<experiment_name>` under `model/`
    model_dir = os.path.join(ROOT_PATH, f"model/{experiment_name}")
    file_util.create_folder(model_dir)

    corpus = _init_corpus(tgt_corpus, f"{data_dir}/{sentence_encoder}-annoy_index.ann", sentence_encoder)
    current_iteration = starting_iteration
    while True:
        print(f"Current iteration: {current_iteration}")
        # Create sub-folder `<current_iteration>` under `data_dir`
        prev_sub_data_dir = os.path.join(ROOT_PATH, f"{data_dir}/{current_iteration - 1}")
        sub_data_dir = f"{data_dir}/{current_iteration}"
        file_util.create_folder(sub_data_dir)

        _resolve_data_path(yaml_config, sub_data_dir)
        _resolve_model_path(yaml_config, model_dir, current_iteration)

        if current_iteration == 0:
            # Bootstrap pseudo-parallel corpus
            source_output_path = f"{sub_data_dir}/{PARALLEL_SOURCE}"
            target_output_path = f"{sub_data_dir}/{PARALLEL_TARGET}"
            _bootstrap_parallel(corpus, src_corpus, similarity_threshold, source_output_path, target_output_path)
        else:
            # Refine pseudo-parallel corpus
            source_parallel_path = f"{prev_sub_data_dir}/{PARALLEL_SOURCE}"
            target_parallel_path = f"{prev_sub_data_dir}/{PARALLEL_TARGET}"
            candidate_json_path = f"{prev_sub_data_dir}/{RESULT_JSON}"
            source_output_path = f"{sub_data_dir}/{PARALLEL_SOURCE}"
            target_output_path = f"{sub_data_dir}/{PARALLEL_TARGET}"

            update_rate = _refine_parallel(corpus, source_parallel_path, target_parallel_path, candidate_json_path,
                                           source_output_path, target_output_path)

            if update_rate < min_update_rate:
                # Terminate if update rate is less than the specified value
                print("Done.")
                exit(1)

        print("Splitting data set...")
        _run_python_script(PREPARE_DATASET_SCRIPT, yaml_config)

        print("Pre-processing data set...")
        _run_python_script(PREPROCESS_SCRIPT, yaml_config)

        print("Training neural machine translation model...")
        _run_python_script(TRAIN_SCRIPT, yaml_config)

        print("Translating...")
        _run_python_script(TRANSLATE_SCRIPT, yaml_config)

        print("Formatting output...")
        _run_python_script(FORMAT_OUTPUT_SCRIPT, yaml_config)

        current_iteration += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Configuration file (.yml) for all scripts")
    parser.add_argument("iteration", type=int, nargs='?', default=0, help="Continue at specific iteration")
    args = parser.parse_args()

    main(args.config, starting_iteration=args.iteration)
