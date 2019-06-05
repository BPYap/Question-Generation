import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__)) + "/../"

MODEL_DIR = ROOT_DIR + "model/"
PRETRAINED_DIR = MODEL_DIR + "pretrained/"

DATA_DIR = ROOT_DIR + "data/"
SOURCE_CORPUS_PATH = DATA_DIR + "source.txt"
DESTINATION_CORPUS_PATH = DATA_DIR + "destination.txt"
