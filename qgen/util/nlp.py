import en_core_web_md
import wmd

_spacy_cache = None


def _get_spacy_model():
    global _spacy_cache
    if _spacy_cache is None:
        _spacy_cache = en_core_web_md.load()
        _spacy_cache.add_pipe(wmd.WMD.SpacySimilarityHook(_spacy_cache), last=True)

    return _spacy_cache


def tokenize(sentence):
    nlp = _get_spacy_model()

    return [token.text for token in nlp(sentence)]


def get_word_mover_dist(sentence1, sentence2):
    nlp = _get_spacy_model()

    return nlp(sentence1).similarity(nlp(sentence2))
