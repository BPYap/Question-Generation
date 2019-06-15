import spacy

_nlp_cache = None


def tokenize(sentence):
    global _nlp_cache
    if _nlp_cache is None:
        _nlp_cache = spacy.load("en_core_web_sm")

    return [token.text for token in _nlp_cache(sentence)]
