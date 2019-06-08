import numpy as np


class BaseEncoder:
    def __init__(self, name, dimension, model_path):
        self.name = name
        self.dimension = dimension
        self.model_path = model_path

    def get_vector(self, sentence):
        raise NotImplementedError("'get_vector' is not implemented")

    def get_vectors(self, sentences):
        vectors = []
        for sentence in sentences:
            vectors.append(self.get_vector(sentence))

        return np.array(vectors)
