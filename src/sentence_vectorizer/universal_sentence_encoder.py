import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

from .base import BaseVectorizer
from ..config import PRETRAINED_DIR


class USEVectorizer(BaseVectorizer):
    def __init__(self):
        super().__init__("Universal Sentence Encoder", PRETRAINED_DIR + "universal_sentence_encoder")

        def init():
            tf.logging.set_verbosity(tf.logging.ERROR)
            with tf.Graph().as_default():
                sentence_placeholder = tf.placeholder(tf.string)
                model = hub.Module(self.model_path)
                vectorize = model(sentence_placeholder)
                session = tf.train.MonitoredSession()

            return lambda sentences: np.array(session.run(vectorize, {sentence_placeholder: sentences}))

        self.vectorize = init()

    def get_vector(self, sentence):
        return self.get_vectors([sentence])[0]

    def get_vectors(self, sentences):
        return self.vectorize(sentences)
