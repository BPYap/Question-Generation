from qgen.corpusbuilder.builder import Builder
from qgen.encoder.glove import GloveEncoder
from script.config import SOURCE_CORPUS_PATH, DESTINATION_CORPUS_PATH, OUTPUT_CORPUS_PATH, GLOVE_MODEL_PATH

if __name__ == '__main__':
    builder = Builder(SOURCE_CORPUS_PATH, DESTINATION_CORPUS_PATH, OUTPUT_CORPUS_PATH)
    builder.set_encoder(GloveEncoder(GLOVE_MODEL_PATH))
    builder.generate_parallel_corpus()
