import fastText

from .base import BaseVectorizer
from ..config import PRETRAINED_DIR


class FTVectorizer(BaseVectorizer):
    def __init__(self):
        super().__init__("fastText", PRETRAINED_DIR + "fastText/cc.en.300.bin")

        self.model = fastText.load_model(self.model_path)

    def get_vector(self, sentence):
        return self.model.get_sentence_vector(sentence)
