from qgen.corpusbuilder.builder import Builder
from qgen.encoder.universal_sentence_encoder import USEEncoder
from qgen.util.config import load_yaml_config

if __name__ == '__main__':
    yaml_config = load_yaml_config()
    src_path = yaml_config['source_corpus_path']
    tgt_path = yaml_config['target_corpus_path']
    src_parallel_path = yaml_config['source_parallel_corpus_path']
    tgt_parallel_path = yaml_config['target_parallel_corpus_path']
    use_path = yaml_config['use_model_path']

    builder = Builder(src_path, tgt_path, src_parallel_path, tgt_parallel_path)
    builder.set_encoder(USEEncoder(use_path))
    builder.generate_parallel_corpus()
