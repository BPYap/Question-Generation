import spacy

from .base import BaseEncoder
from ..config import PRETRAINED_DIR


class GloveEncoder(BaseEncoder):
    def __init__(self):
        super().__init__("Average GloVe", 300, PRETRAINED_DIR + "spacy_glove/en_vectors_web_lg-2.1.0")

        self.nlp = spacy.load(self.model_path)

    def get_vector(self, sentence):
        return self.nlp(sentence).vector
