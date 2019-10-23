import itertools
import string

from tqdm import tqdm

from qgen.util import nlp
from .matcher import FuzzyMatcher
from .pattern import pattern_specs
from ..base import BaseGenerator

# 5W1H
WH = {'who', 'what', 'why', 'where', 'when', 'how'}
# Coordinating conjunction
FANBOYS = {'for', 'and', 'nor', 'but', 'or', 'yet', 'so'}


class FPMGenerator(BaseGenerator):
    """ Generate questions via fuzzy pattern matching on existing question patterns. """

    def __init__(self):
        super().__init__("Fuzzy Question Pattern Matching")

        self.patterns = self._generate_patterns(pattern_specs)
        self.matcher = FuzzyMatcher(self.patterns)

    @staticmethod
    def _generate_patterns(specs):
        patterns = []
        for group in specs:
            for _ in range(len(group['patterns'])):  # iterate through all original patterns
                pattern = group['patterns'].pop(0).strip()
                tokens_list = []  # list of tokens that require substitution
                for word in pattern.split():
                    if word.startswith('{') and word.endswith('}'):
                        tokens_list.append(word[1:-1])
                temp = [pattern]
                for token in tokens_list:
                    for _ in range(len(temp)):  # iterate through all sub-patterns
                        curr_pattern = temp.pop(0)
                        for substitute in group['substitution_keys'][token]:
                            temp.append(curr_pattern.replace('{' + token + '}', substitute))
                group['patterns'].extend(temp)

            patterns.append(group['patterns'])

        return patterns

    @staticmethod
    def _format_input(sentence):
        """ Add a space after specific punctuation if it is not followed by a space
        """
        punctuations = "!),.:;?]}"
        char_array = []
        for i, s in enumerate(sentence):
            char_array.append(s)
            if i < len(sentence) - 1 and s in punctuations and sentence[i + 1] not in punctuations + " ":
                char_array.append(" ")

        return "".join(char_array)

    @staticmethod
    def _format_output(sentence):
        words = sentence.strip("!,.:;?").split()
        words[0] = words[0][0].upper() + words[0][1:]  # capitalize first letter
        words[-1] = words[-1] + "?"

        return " ".join(words)

    @staticmethod
    def _has_multiple_question(question):
        """ Simple heuristic to determine whether a `question` contains multiple sub-questions.
        """
        if question.count('?') > 1:
            return True
        else:
            combined_wh = [["{} and {}".format(w1, w2), "{} & {}".format(w1, w2)] for w1 in WH for w2 in WH]
            return any([c in question.lower() for c in itertools.chain.from_iterable(combined_wh)])

    @staticmethod
    def _split_question(question):
        spacy_nlp = nlp.get_spacy_model()

        def _resolve_followup_question(prev_question, followup_question):
            """ Resolve sentences start with "If so", "If not", etc.
            """
            sub_question_lower = followup_question.lower()
            if any(sub_question_lower.startswith(pre) for pre in ['if so', 'if not']):
                last_aux_index = -1
                last_sub_index = -1
                index = 0
                with spacy_nlp.disable_pipes('ner'):
                    for token in spacy_nlp(prev_question):
                        if token.dep_ == 'aux':
                            last_aux_index = index
                        elif token.dep_ in ['nsubj', 'nsubjpass']:
                            last_sub_index = index
                        elif token.dep_ == 'ROOT':
                            break

                        if token.dep_ not in ['case', 'punct']:
                            index += 1

                tokens = prev_question.rstrip(".!?, ").split()
                sub = " ".join(tokens[last_aux_index + 1:last_sub_index + 1])
                aux = tokens[last_aux_index].lower()
                sub_sent = " ".join(tokens[last_sub_index + 1:]) + ","
                followup_question = " ".join(followup_question.split()[2:])
                if sub_question_lower.startswith('if so'):
                    followup_question = " ".join(["If", sub, aux, sub_sent, followup_question])
                elif sub_question_lower.startswith('if not'):
                    followup_question = " ".join(["If", sub, aux, "not", sub_sent, followup_question])

            return followup_question

        if not FPMGenerator._has_multiple_question(question):
            return [question]

        result = []
        with spacy_nlp.disable_pipes('ner'):
            doc = spacy_nlp(question)

            for sent in doc.sents:
                # remove leading coordinating conjunction
                for cc in FANBOYS:
                    if sent.text.lower().startswith(cc):
                        result.append(sent.text[len(cc) + 1:])
                        break
                else:
                    if len(result) >= 1 and any(sent.text.lower().startswith(pre) for pre in ['if so', 'if not']):
                        result.append(_resolve_followup_question(result[0], sent.text))
                    else:
                        result.append(sent.text)

        context = ""
        combined_wh = [["{} and {}".format(w1, w2), "{} & {}".format(w1, w2)] for w1 in WH for w2 in WH]
        for q in result.copy():
            if q.endswith('.'):
                context = q + ' '
                result.remove(q)
                continue

            for phrase in itertools.chain.from_iterable(combined_wh):
                if phrase in q.lower():
                    result.remove(q)
                    start_index = q.lower().index(phrase) + len(phrase)
                    sub_question = q[start_index:]
                    temp = phrase.split()
                    result.extend([temp[0].title() + sub_question, temp[-1].title() + sub_question])
                    break

        if context:
            results = [context + s for s in result]
        else:
            results = [nlp.resolve_coref(s, question) for s in result]

        return results

    @staticmethod
    def _preprocess(question):
        # 1. Convert contraction to regular form (e.g. "What's" to "What is")
        question = nlp.convert_contraction(FPMGenerator._format_input(question).strip())

        # 2. Separate multiple questions from sentence
        sentences = [question]
        if FPMGenerator._has_multiple_question(question):
            sentences = FPMGenerator._split_question(question)

        return sentences

    def generate(self, sentence):
        inputs = self._preprocess(sentence)

        result = []
        for sentence in inputs:
            # Extract question pattern
            matched_result = self.matcher.match(sentence)

            if not matched_result:
                continue
            else:
                tokens = matched_result.tokens
                if len(tokens['<st>']) > 1:
                    # concatenate multiple statements into single statement
                    tokens['<st>'] = [
                        ' and '.join(tokens['<st>']).translate(str.maketrans('', '', string.punctuation))]

                # Substitute tokens into other question patterns
                patterns_list = self.patterns[matched_result.group_id]
                for pattern in patterns_list:
                    if pattern.lower() == matched_result.pattern.lower():
                        continue
                    pattern_tokens = pattern.split()
                    if (len(tokens['<sbj>']) == pattern_tokens.count('<sbj>') and
                            len(tokens['<obj>']) >= pattern_tokens.count('<obj>') and
                            len(tokens['<act>']) == pattern_tokens.count('<act>') and
                            len(tokens['<st>']) >= pattern_tokens.count('<st>')):
                        for i in range(pattern_tokens.count('<obj>')):
                            pattern_tokens[pattern_tokens.index('<obj>')] = tokens['<obj>'][i].strip('?')
                        for i in range(pattern_tokens.count('<sbj>')):
                            pattern_tokens[pattern_tokens.index('<sbj>')] = tokens['<sbj>'][i].strip('?')
                        for i in range(pattern_tokens.count('<act>')):
                            pattern_tokens[pattern_tokens.index('<act>')] = tokens['<act>'][i].strip('?')
                        for i in range(pattern_tokens.count('<st>')):
                            pattern_tokens[pattern_tokens.index('<st>')] = tokens['<st>'][i].strip('?')

                        # Coreference resolution (i.e. Find out what 'it' in a sentence is referring to)
                        permuted = ' '.join(pattern_tokens)
                        if tokens['<st>'] and pattern.split().count('<st>') == 0:
                            result.append(self._format_output(
                                nlp.resolve_coref(permuted, sentence))
                            )
                        else:
                            result.append(self._format_output(permuted))

                result = list(set(result).difference({sentence}))

        return result

    def batch_generate(self, sentences):
        results = dict()
        for sentence in tqdm(sentences):
            results[sentence] = self.generate(sentence)

        return results
