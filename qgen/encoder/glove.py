import spacy

from .base import BaseEncoder


class GloveEncoder(BaseEncoder):
    def __init__(self, model_path):
        super().__init__("Average GloVe", 300, model_path)

        self.nlp = spacy.load(model_path)

    def get_vector(self, sentence):
        return self.nlp(sentence).vector
