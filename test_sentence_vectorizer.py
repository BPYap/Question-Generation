from src.sentence_vectorizer.fast_text import FTVectorizer
from src.sentence_vectorizer.glove import GloveVectorizer
from src.sentence_vectorizer.universal_sentence_encoder import USEVectorizer


if __name__ == '__main__':
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
    # vectorizers = [FTVectorizer(), GloveVectorizer(), USEVectorizer()]
    vectorizers = [GloveVectorizer()]

    for i, sentence in enumerate(sentences):
        print("=" * 80)
        print("Sentence: {}\n".format(sentence))
        for vectorizer in vectorizers:
            print("Getting vector from {}...".format(vectorizer.name))
            vector = vectorizer.get_vector(sentence)
            print("Vector: [{}, ...]".format(", ".join(str(x) for x in vector[:3])))
            print("Vector dimensions: {}\n".format(len(vector)))

    for vectorizer in vectorizers:
        print("Getting vectors from {}...".format(vectorizer.name))
        vectors = vectorizer.get_vectors(sentences)
        print("[")
        for vector in vectors:
            print(" [{}, ...]".format(", ".join(str(x) for x in vector[:3])))
        print("]")
        print("Vectors dimensions: {}\n".format(vectors.shape))
