import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__)) + "/../"

MODEL_DIR = ROOT_DIR + "model/"
PRETRAINED_DIR = MODEL_DIR + "pretrained/"

FASTTEXT_MODEL_PATH = PRETRAINED_DIR + "fastText/cc.en.300.bin"
GLOVE_MODEL_PATH = PRETRAINED_DIR + "spacy_glove/en_vectors_web_lg-2.1.0"
USE_MODEL_PATH = PRETRAINED_DIR + "universal_sentence_encoder"

DATA_DIR = ROOT_DIR + "data/"
SOURCE_CORPUS_PATH = DATA_DIR + "source.txt"
DESTINATION_CORPUS_PATH = DATA_DIR + "destination.txt"
OUTPUT_CORPUS_PATH = DATA_DIR + "output.txt"
