class BaseVectorizer:
    def __init__(self, name, model_path):
        self.name = name
        self.model_path = model_path

    def get_vector(self, sentence):
        raise NotImplementedError("'get_vector' is not implemented")
