from qgen.corpusbuilder.builder import Builder
from qgen.encoder.fasttext import FTEncoder
from qgen.encoder.glove import GloveEncoder
from qgen.encoder.universal_sentence_encoder import USEEncoder
from qgen.util.config import load_yaml_config

if __name__ == '__main__':
    yaml_config = load_yaml_config()
    src_path = yaml_config['source_corpus_path']
    tgt_path = yaml_config['target_corpus_path']
    src_parallel_path = yaml_config['source_parallel_corpus_path']
    tgt_parallel_path = yaml_config['target_parallel_corpus_path']
    fasttext_path = yaml_config['fasttext_model_path']
    glove_path = yaml_config['glove_model_path']
    use_path = yaml_config['use_model_path']
    encoder = yaml_config['encoder']

    builder = Builder(src_path, tgt_path, src_parallel_path, tgt_parallel_path)

    if encoder == 'fasttext':
        builder.set_encoder(FTEncoder(fasttext_path))
    elif encoder == 'glove':
        builder.set_encoder(GloveEncoder(glove_path))
    else:
        builder.set_encoder(USEEncoder(use_path))

    builder.build_parallel_corpus()
