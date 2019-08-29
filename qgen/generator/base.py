class BaseGenerator:
    def __init__(self, name):
        self.name = name

    def generate(self, sentence):
        raise NotImplementedError("'generate' is not implemented")

    def batch_generate(self, sentences):
        raise NotImplementedError("'batch_generate' is not implemented")
