import fasttext

from .base import BaseEncoder


class FTEncoder(BaseEncoder):
    def __init__(self, model_path):
        super().__init__("fastText", 300, model_path)

        self.model = fasttext.load_model(self.model_path)

    def get_vector(self, sentence):
        return self.model.get_sentence_vector(sentence)
