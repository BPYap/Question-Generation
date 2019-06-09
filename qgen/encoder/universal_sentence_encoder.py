import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

from .base import BaseEncoder


class USEEncoder(BaseEncoder):
    def __init__(self, model_path):
        super().__init__("Universal Sentence Encoder", 512, model_path)

        def init():
            tf.logging.set_verbosity(tf.logging.ERROR)
            with tf.Graph().as_default():
                sentence_placeholder = tf.placeholder(tf.string)
                model = hub.Module(self.model_path)
                encode_sentence = model(sentence_placeholder)
                session = tf.train.MonitoredSession()

            return lambda sentences: np.array(session.run(encode_sentence, {sentence_placeholder: sentences}))

        self.encode_sentences = init()

    def get_vector(self, sentence):
        return self.get_vectors([sentence])[0]

    def get_vectors(self, sentences):
        return self.encode_sentences(sentences)
