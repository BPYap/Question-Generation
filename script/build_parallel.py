import argparse

from qgen.corpusbuilder.builder import Builder
from qgen.encoder.fasttext import FTEncoder
from qgen.encoder.glove import GloveEncoder
from qgen.encoder.universal_sentence_encoder import USEEncoder
from qgen.util.config import load_yaml_config


def main(src_path, tgt_path, src_parallel_path, tgt_parallel_path, encoder):
    pretrained_config = load_yaml_config("config/pretrained.yml")
    fasttext_path = pretrained_config['fasttext_model_path']
    glove_path = pretrained_config['glove_model_path']
    use_path = pretrained_config['use_model_path']

    builder = Builder(src_path, tgt_path, src_parallel_path, tgt_parallel_path)

    if encoder == 'fasttext':
        builder.set_encoder(FTEncoder(fasttext_path))
    elif encoder == 'glove':
        builder.set_encoder(GloveEncoder(glove_path))
    else:
        builder.set_encoder(USEEncoder(use_path))

    builder.build_parallel_corpus()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--src")
    parser.add_argument("--tgt")
    parser.add_argument("--parallel_src")
    parser.add_argument("--parallel_tgt")
    parser.add_argument("--encoder")
    args = parser.parse_args()

    main(args.src, args.tgt, args.parallel_src, args.parallel_tgt, args.encoder)
