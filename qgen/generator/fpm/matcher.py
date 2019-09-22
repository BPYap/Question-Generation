import re
from collections import defaultdict
from itertools import product

import regex

from qgen.util import nlp
from .pattern import TOKENS as SPECIAL_TOKENS

_spacy_docs_cache = dict()


class MatchedResult:
    def __init__(self, group_id, pattern, match):
        self.group_id = group_id
        self.pattern = pattern
        self.fuzzy_counts = sum(match.fuzzy_counts)
        self.tokens = self._parse_tokens(match.string, pattern, match)

    @staticmethod
    def _get_spacy_doc(sentence):
        spacy_nlp = nlp.get_spacy_model()
        if sentence not in _spacy_docs_cache:
            with spacy_nlp.disable_pipes('ner'):
                _spacy_docs_cache[sentence] = spacy_nlp(sentence)

        return _spacy_docs_cache[sentence]

    @staticmethod
    def _get_first_verb_offset(sentence, starting_offset=0):
        """ Return character offset for the first encountered verb
        """
        doc = MatchedResult._get_spacy_doc(sentence)
        for token in doc:
            if token.idx < starting_offset:
                continue
            # single verb or adverb-verb pair
            elif token.pos_ == 'VERB' or (
                    token.tag_ == 'RB' and (token.i + 1 < len(doc) and doc[token.i + 1].pos_ == 'VERB')
            ):
                return token.idx

        return -1

    @staticmethod
    def _is_subj(sentence, substr):
        """ Returns True if `substr` in `sentence` is a noun chunk and its syntactic dependency tag is nominal subject
        """
        # remove punctuations to make things easier
        sentence = " ".join(nlp.replace_punct(sentence, replace_with=" ", ignore_list="-").strip().split())
        substr = " ".join(nlp.replace_punct(substr, replace_with=" ", ignore_list="-").strip().split())

        doc = MatchedResult._get_spacy_doc(sentence)
        temp = []
        sbj_tags = ['nsubj', 'nsubjpass']
        previous_dep = None
        for chunk in doc.noun_chunks:
            if chunk.text == substr and chunk.root.dep_ in sbj_tags:
                return True
            elif chunk.text in nlp.get_ngrams(substr, len(chunk.text.split())):
                # sometimes the subject might be combination of chunks, so we're keeping this chunk for later
                # *Note: Consecutive subject chunk is discarded since they are two separate and not
                # related noun chunks. (i.e. If they belongs to same chunk, they'd be grouped together as
                # a chunk, not as 2 separate chunks)
                if not (previous_dep in sbj_tags and chunk.root.dep_ in sbj_tags):
                    temp.append(chunk.text)
                    previous_dep = chunk.root.dep_

        if temp and substr.startswith(temp[0]) and substr.endswith(temp[-1]):
            return True

        return False

    @staticmethod
    def _parse_tokens(sentence, pattern, match):
        tokens = defaultdict(list)
        for t in SPECIAL_TOKENS:
            if t in pattern:
                tokens[t] = match.captures(t[1:-1])

        # resolve <sbj> <act> and <obj> <act>
        if "<sbj> <act>" in pattern or "<obj> <act>" in pattern:
            pairs = list(product(tokens['<sbj>'] if "<sbj> <act>" in pattern else tokens['<obj>'], tokens['<act>']))
            unresolved = []
            for pair in pairs:
                if " ".join(pair) in sentence:
                    unresolved.append(pair)

            for pair in unresolved:
                sub_sentence = " ".join(pair)
                verb_offset = MatchedResult._get_first_verb_offset(sentence, sentence.index(sub_sentence))
                if verb_offset == -1:
                    tokens = defaultdict(list)
                    break

                second_part = sentence[verb_offset:sentence.index(sub_sentence) + len(sub_sentence)]
                first_part = sub_sentence[:sub_sentence.rfind(second_part)]

                if pair[0] in tokens['<sbj>']:
                    index = tokens['<sbj>'].index(pair[0])
                    tokens['<sbj>'][index] = first_part
                else:
                    index = tokens['<obj>'].index(pair[0])
                    tokens['<obj>'][index] = first_part

                act_index = tokens['<act>'].index(pair[1])
                tokens['<act>'][act_index] = second_part

        # Verify <sbj> tokens
        for sbj in tokens['<sbj>']:
            if not MatchedResult._is_subj(sentence, sbj):
                tokens = defaultdict(list)

        return tokens


class FuzzyMatcher:
    def __init__(self, patterns):
        self.patterns = [[(pattern, self._convert_to_fuzzy_regex(pattern)) for pattern in group] for group in patterns]

    @staticmethod
    def _convert_to_fuzzy_regex(pattern):
        match_any = '.+'
        fuzzy_rule = '{e<=3}'
        ignore_case = '(?i)'
        space = re.escape(' ')
        placeholder = '<<<placeholder>>>'

        special_tokens = [token for token in pattern.split() if token in SPECIAL_TOKENS]
        pattern = re.escape(pattern)
        for token in SPECIAL_TOKENS:
            pattern = pattern.replace(re.escape(token), match_any)

        parts = pattern.split(match_any)
        for i in range(len(parts)):
            part = parts[i]
            if len(part.strip(space)) != 0:
                add_start = part.startswith(space)
                add_end = part.endswith(space)
                parts[i] = f"{space if add_start else ''}({part.strip(space)}){fuzzy_rule}{space if add_end else ''}"

        fuzzy_regex = rf"{ignore_case}{match_any.join(parts)}"
        # Add named capture groups
        for sp in special_tokens:
            fuzzy_regex = fuzzy_regex.replace(match_any, f"(?{sp}{placeholder})", 1)
        fuzzy_regex = fuzzy_regex.replace(placeholder, match_any)

        return fuzzy_regex

    def match(self, sentence):
        def get_effective_length(_pattern):
            # get pattern length without counting special tokens
            _pattern = _pattern.replace("<sbj>", "")
            _pattern = _pattern.replace("<obj>", "")
            _pattern = _pattern.replace("<act>", "")
            _pattern = _pattern.replace("<st>", "")

            return len(_pattern)

        candidates = []
        for group_id, group in enumerate(self.patterns):
            for pattern, fuzzy_regex in group:
                match = regex.fullmatch(fuzzy_regex, sentence.strip("?"))
                if match is not None:
                    candidates.append(MatchedResult(group_id, pattern, match))

        # sort by least fuzzy count, then by most pattern length
        candidates.sort(key=lambda x: (x.fuzzy_counts, -get_effective_length(x.pattern)))

        return candidates[0] if len(candidates) > 0 else None
