import string

import en_core_web_md
import spacy

_spacy_cache = None
_coref_cache = None

FAST_TOKENIZER = spacy.load('en_core_web_sm', disable=['tagger', 'parser', 'ner', 'textcat'])

# Linguistic Constants
AUXILIARIES = ['am', 'is', 'are', 'was', 'were', 'be', 'could', 'can', 'should', 'shall', 'would', 'will',
               'might', 'may', 'must', 'ought', 'does', 'did', 'do', 'been']
SUBJECTS = ['i', 'me', 'my', 'he', 'him', 'his', 'she', 'her', 'we', 'our', 'us', 'they', 'them', 'their',
            'you', 'your', 'it', 'its']
CONTRACTION = {
    "'tis": "this is",
    "'twas": "this was",
    "ain't": "are not",
    "aren't": "are not",
    "can't": "can not",
    "could've": "could have",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hasn't": "has not",
    "he'd": "he had",
    "he'll": "he will",
    "he's": "he is",
    "how'd": "how do",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'll": "I will",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it's": "it is",
    "might've": "might have",
    "mightn't": "might not",
    "must've": "must have",
    "mustn't": "must not",
    "shan't": "shall not",
    "she'd": "she had",
    "she'll": "she will",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "that'll": "that will",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they had",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "wasn't": "was not",
    "we'd": "we had",
    "we'll": "we will",
    "we're": "we are",
    "weren't": "were not",
    "what'd": "what had",
    "what's": "what is",
    "when'd": "when had",
    "when'll": "when will",
    "when's": "when is",
    "where'd": "where had",
    "where'll": "where will",
    "where's": "where is",
    "who'd": "who had",
    "who'll": "who will",
    "who's": "who is",
    "why'd": "why had",
    "why'll": "why will",
    "why's": "why is",
    "won't": "would not",
    "would've": "would have",
    "wouldn't": "would not",
    "you'd": "you had",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have"
}


def get_spacy_model():
    global _spacy_cache
    if _spacy_cache is None:
        print("Initializing spaCy model...")
        _spacy_cache = en_core_web_md.load()

    return _spacy_cache


def _get_coref_model():
    global _coref_cache

    if _coref_cache is None:
        print("Initializing NeuralCoref model...")
        _coref_cache = spacy.load('en_coref_md', disable=['ner', 'textcat'])

    return _coref_cache


def get_ngrams(sentence, n):
    temp = sentence.split()
    return [' '.join(temp[i:i + n]) for i in range(len(temp) - n + 1)]


def replace_punct(sentence, replace_with="", ignore_list=""):
    """ Replace punctuation in `sentence` with tokens specified by `replace_with`.
    """
    punct = string.punctuation
    for symbol in ignore_list:
        punct = punct.replace(symbol, '')
    if replace_with:
        return sentence.translate(str.maketrans(punct, replace_with * len(punct)))
    else:
        return sentence.translate(str.maketrans('', '', punct))


def convert_contraction(sentence):
    """ Returns converted `sentence` with contradictions replaced. (e.g. "What's" is replaced with "What is")
    """
    tokens = sentence.split()
    for i, t in enumerate(tokens):
        for c in CONTRACTION:
            if t.lower().rstrip(string.punctuation) == c.lower():
                tokens[i] = CONTRACTION[c]
                if t[0].isupper():
                    tokens[i] = tokens[i].capitalize()

    return ' '.join(tokens)


def resolve_coref(sentence, context):
    """ Return a modified sentence with "mentions" replaced by the main entity
    """
    coref_model = _get_coref_model()
    doc = coref_model(context)
    if not doc._.has_coref:
        return sentence
    else:
        # get the phrase surrounding the mention
        sent_tokens = [token.text for token in FAST_TOKENIZER(sentence)]
        for cluster in doc._.coref_clusters:
            for span in cluster.mentions:
                if cluster.main.text.lower() in SUBJECTS or span.text.lower() == cluster.main.text.lower() \
                        or cluster.main.text in sentence:
                    # Don't resolve coreference if any of the following is true:
                    #    1. Cluster.main.text (the phrase which the mention is resolved to) is in the SUBJECTS list,
                    #       since they are not what we're looking for (e.g. mention = "a boy", Cluster.main.text = "he")
                    #    2. Mention and Cluster.main.text are the same
                    #    3. Cluster.main.text is already in the output sentence
                    continue

                if span.text.lower() == 'it':  # heuristic to gather more context if mention is the word 'it'
                    index = span.start
                    if index == len(
                            doc) - 1:  # if mention is the last word in doc, we take the last 3 tokens as phrase
                        phrase = doc[index - 2:].text
                    else:  # else we take one word before the mention and one word after the mention to form a phrase
                        phrase = doc[index - 1:index + 2].text
                else:
                    phrase = span.text

                phrase = phrase.strip(string.punctuation)  # remove leading and ending punctuation
                phrase_len = len(phrase.split())

                # check if phrase is in sent_doc
                for j in range(len(sent_tokens)):
                    if " ".join(sent_tokens[j: j + phrase_len]) == phrase:
                        # delete mention and insert the main entity
                        start = j + sent_tokens[j:].index(span[0].text)
                        end = j + sent_tokens[j:].index(span[-1].text)
                        sent_tokens = sent_tokens[:start] + sent_tokens[end + 1:]
                        sent_tokens.insert(start, cluster.main.text)
                        break

        return " ".join(sent_tokens)
