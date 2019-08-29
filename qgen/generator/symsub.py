import string
from itertools import product

import numpy as np
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from tqdm import tqdm

from .base import BaseGenerator
from ..util.nlp import get_spacy_model, tokenize


class SymSubGenerator(BaseGenerator):
    """ Generate questions via sense-disambiguated synonyms substitution. """

    def __init__(self, encoder, discount_factor=0.5, threshold=0.5):
        """
        :param encoder: encoder for the computation of sentence embeddings
        :param discount_factor: discount factor for weightage calculation during word sense disambiguation (wsd)
        :param threshold: threshold value ranging from 0 to 1 for wsd score.
        """
        super().__init__("Sense-disambiguated Synonym Substitution")

        self.discount_factor = discount_factor
        self.threshold = threshold
        self.encoder = encoder

    def _get_best_sense_key(self, sentence, lemma, pos):
        def _compute_weightage(main_synset, related_synset):
            distance = main_synset.shortest_path_distance(related_synset)
            if distance is None:
                return 1
            else:
                return 1 / (1 + distance)

        wordnet_pos = {'VERB': wn.VERB, 'NOUN': wn.NOUN, 'ADJ': wn.ADJ, 'ADV': wn.ADV}
        if pos not in wordnet_pos:
            return None

        results = []  # tuple of lemma and average similarity score
        lemma_count = 0
        for synset in wn.synsets(lemma, pos=wordnet_pos[pos]):
            if lemma.lower() not in [l.name().lower() for l in synset.lemmas()]:
                continue

            extended_gloss = {synset.definition(): 1}  # gloss and weightage map
            for s in synset.hypernyms():
                extended_gloss[s.definition()] = _compute_weightage(synset, s)
                for e in s.examples():
                    extended_gloss[e] = extended_gloss[s.definition()] * self.discount_factor

            for s in synset.hyponyms():
                extended_gloss[s.definition()] = _compute_weightage(synset, s)
                for e in s.examples():
                    extended_gloss[e] = extended_gloss[s.definition()] * self.discount_factor

            for s in synset.verb_groups():
                extended_gloss[s.definition()] = _compute_weightage(synset, s)
                for e in s.examples():
                    extended_gloss[e] = extended_gloss[s.definition()] * self.discount_factor

            for s in synset.similar_tos():
                extended_gloss[s.definition()] = _compute_weightage(synset, s)
                for e in s.examples():
                    extended_gloss[e] = extended_gloss[s.definition()] * self.discount_factor

            for lemma_ in synset.lemmas():
                if lemma_.name().lower() == lemma.lower():
                    for s in [l.synset() for l in lemma_.derivationally_related_forms()]:
                        extended_gloss[s.definition()] = _compute_weightage(synset, s)
                    break

            for e in synset.examples():
                extended_gloss[e] = 1

            sentences = [sentence] + list(extended_gloss.keys())
            embeddings = self.encoder.get_vectors(sentences)
            similarity_matrix = np.inner(embeddings, embeddings)

            score = 0
            weightage = list(extended_gloss.values())
            for i in range(1, len(similarity_matrix)):
                score += similarity_matrix[0][i] * weightage[i - 1]

            for lemma_ in synset.lemmas():
                if lemma_.name().lower() == lemma.lower():
                    lemma_count += lemma_.count()
                    results.append((lemma_, score))
                    break

        if not results:
            return None

        sense_count = len(results)
        results = [(l.key(), s * ((l.count() + 1) / (lemma_count + sense_count))) for l, s in results]
        # print(sorted(results, key=lambda r: r[1], reverse=True))
        return sorted(results, key=lambda r: r[1], reverse=True)[0][0]

    def _get_synonyms(self, sentence, word):
        if not sentence or not word or word.lower() in stopwords.words('english') or len(word.split()) > 1:
            return []

        nlp = get_spacy_model()
        doc = nlp(sentence)
        # ignore `word` that is a part of noun_chunk
        for noun_chunk in doc.noun_chunks:
            tokens = [t.strip(string.punctuation) for t in noun_chunk.text.split()
                      if t.strip(string.punctuation).lower() not in stopwords.words('english')]
            if len(tokens) > 1 and word in tokens:
                return []

        for token in doc:
            if token.text == word:
                key = self._get_best_sense_key(sentence, token.lemma_, token.pos_)
                if key is None:
                    return []
                else:
                    return [w.replace("_", " ") for w in wn.lemma_from_key(key).synset().lemma_names()
                            if w.lower() != token.lemma_.lower()]

    def generate(self, sentence):
        tokens = tokenize(sentence)
        tokens_for_sub = [token for token in tokens if tokens.count(token) == 1]
        token2synonyms = dict()
        for token in tokens_for_sub:
            syms = self._get_synonyms(sentence, token)
            if syms:
                token2synonyms[token] = [token] + syms

        result = []
        keys = list(token2synonyms.keys())
        combinations = product(*token2synonyms.values())
        for combination in combinations:
            temp = tokens.copy()
            for i, sub_token in enumerate(combination):
                key = keys[i]
                temp[temp.index(key)] = sub_token

            result.append(' '.join(temp))

        return result

    def batch_generate(self, sentences):
        print(f"Generating questions via {self.name}...")
        result = dict()
        for sentence in tqdm(sentences):
            result[sentence] = self.generate(sentence)

        return result
