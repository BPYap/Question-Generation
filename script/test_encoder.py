from qgen.encoder.fasttext import FTEncoder
from qgen.encoder.glove import GloveEncoder
from qgen.encoder.universal_sentence_encoder import USEEncoder
from qgen.util.config import load_yaml_config


if __name__ == '__main__':
    yaml_config = load_yaml_config()
    fasttext_path = yaml_config['fasttext_model_path']
    glove_path = yaml_config['glove_model_path']
    use_path = yaml_config['use_model_path']

    sentences = [
        "How can my organisation apply to be a Baby Bonus Approved Institution?",
        "I have entered the Unique Entity Number (UEN) using 'Join as an Approved Institution (AI)' service, "
        "but your system does not have matching records of my Unique Entity Number (UEN). "
        "Can I still submit my application?",
        "I have entered the Unique Entity Number (UEN) using the 'Join as Approved Institution (AI)' service, "
        "but your system indicated that my Unique Entity Number (UEN) is invalid, what should I do?",
        "Is there a validity period to be a Baby Bonus Approved Institution?",
        "How much does an organisation need to pay to register as an Approved Institution (AI) with "
        "Ministry of Social and Family Development (MSF)?",
        ]
    encoders = [FTEncoder(fasttext_path), GloveEncoder(glove_path), USEEncoder(use_path)]

    for i, sentence in enumerate(sentences):
        print("=" * 80)
        print("Sentence: {}\n".format(sentence))
        for encoder in encoders:
            print("Getting vector from {}...".format(encoder.name))
            vector = encoder.get_vector(sentence)
            print("Vector: [{}, ...]".format(", ".join(str(x) for x in vector[:3])))
            print("Vector dimensions: {}\n".format(len(vector)))

    for encoder in encoders:
        print("Getting vectors from {}...".format(encoder.name))
        vectors = encoder.get_vectors(sentences)
        print("[")
        for vector in vectors:
            print(" [{}, ...]".format(", ".join(str(x) for x in vector[:3])))
        print("]")
        print("Vectors dimensions: {}\n".format(vectors.shape))
