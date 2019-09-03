# Easy data augmentation techniques for text classification
# Jason Wei and Kai Zou
# Original codes adapted from https://github.com/jasonwei20/eda_nlp

import random
import re
from random import shuffle

from nltk.corpus import wordnet
from tqdm import tqdm

from .base import BaseGenerator

random.seed(42)

STOP_WORDS = ['i', 'me', 'my', 'myself', 'we', 'our',
              'ours', 'ourselves', 'you', 'your', 'yours',
              'yourself', 'yourselves', 'he', 'him', 'his',
              'himself', 'she', 'her', 'hers', 'herself',
              'it', 'its', 'itself', 'they', 'them', 'their',
              'theirs', 'themselves', 'what', 'which', 'who',
              'whom', 'this', 'that', 'these', 'those', 'am',
              'is', 'are', 'was', 'were', 'be', 'been', 'being',
              'have', 'has', 'had', 'having', 'do', 'does', 'did',
              'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
              'because', 'as', 'until', 'while', 'of', 'at',
              'by', 'for', 'with', 'about', 'against', 'between',
              'into', 'through', 'during', 'before', 'after',
              'above', 'below', 'to', 'from', 'up', 'down', 'in',
              'out', 'on', 'off', 'over', 'under', 'again',
              'further', 'then', 'once', 'here', 'there', 'when',
              'where', 'why', 'how', 'all', 'any', 'both', 'each',
              'few', 'more', 'most', 'other', 'some', 'such', 'no',
              'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
              'very', 's', 't', 'can', 'will', 'just', 'don',
              'should', 'now', '']


class EDAGenerator(BaseGenerator):
    """ Generate questions via Easy Data Augmentation Techniques (Reference: https://arxiv.org/abs/1901.11196). """

    def __init__(self, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, p_rd=0.1, num_aug=9):
        """
        :param alpha_sr: ratio of words to be replaced by synonyms
        :param alpha_ri: ratio of words to be inserted
        :param alpha_rs: ratio of words to be swapped
        :param p_rd: probability that a word will be deleted
        :param num_aug: number of augmentations
        """
        super().__init__("Easy Data Augmentation Techniques")

        self.alpha_sr = alpha_sr
        self.alpha_ri = alpha_ri
        self.alpha_rs = alpha_rs
        self.p_rd = p_rd
        self.num_aug = num_aug

    @staticmethod
    def _get_only_chars(line):
        clean_line = ""

        line = line.replace("’", "")
        line = line.replace("'", "")
        line = line.replace("-", " ")  # replace hyphens with spaces
        line = line.replace("\t", " ")
        line = line.replace("\n", " ")
        line = line.lower()

        for char in line:
            if char in 'qwertyuiopasdfghjklzxcvbnm ':
                clean_line += char
            else:
                clean_line += ' '

        clean_line = re.sub(' +', ' ', clean_line)  # delete extra spaces
        if clean_line[0] == ' ':
            clean_line = clean_line[1:]
        return clean_line

    @staticmethod
    def _get_synonyms(word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonym = l.name().replace("_", " ").replace("-", " ").lower()
                synonym = "".join([char for char in synonym if char in ' qwertyuiopasdfghjklzxcvbnm'])
                synonyms.add(synonym)
        if word in synonyms:
            synonyms.remove(word)
        return list(synonyms)

    @staticmethod
    def _synonym_replacement(words, n):
        """ Replace n words in the sentence with synonyms from wordnet.
        """
        new_words = words.copy()
        random_word_list = list(set([word for word in words if word not in STOP_WORDS]))
        random.shuffle(random_word_list)
        num_replaced = 0
        for random_word in random_word_list:
            synonyms = EDAGenerator._get_synonyms(random_word)
            if len(synonyms) >= 1:
                synonym = random.choice(list(synonyms))
                new_words = [synonym if word == random_word else word for word in new_words]
                num_replaced += 1
            if num_replaced >= n:  # only replace up to n words
                break

        # this is stupid but we need it, trust me
        sentence = ' '.join(new_words)
        new_words = sentence.split(' ')

        return new_words

    @staticmethod
    def _random_deletion(words, p):
        """ Randomly delete words from the sentence with probability p.
        """
        # obviously, if there's only one word, don't delete it
        if len(words) == 1:
            return words

        # randomly delete words with probability p
        new_words = []
        for word in words:
            r = random.uniform(0, 1)
            if r > p:
                new_words.append(word)

        # if you end up deleting all words, just return a random word
        if len(new_words) == 0:
            rand_int = random.randint(0, len(words) - 1)
            return [words[rand_int]]

        return new_words

    @staticmethod
    def _swap_word(new_words):
        random_idx_1 = random.randint(0, len(new_words) - 1)
        random_idx_2 = random_idx_1
        counter = 0
        while random_idx_2 == random_idx_1:
            random_idx_2 = random.randint(0, len(new_words) - 1)
            counter += 1
            if counter > 3:
                return new_words
        new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
        return new_words

    @staticmethod
    def _random_swap(words, n):
        """ Randomly swap two words in the sentence n times
        """
        new_words = words.copy()
        for _ in range(n):
            new_words = EDAGenerator._swap_word(new_words)
        return new_words

    @staticmethod
    def _add_word(new_words):
        synonyms = []
        counter = 0
        while len(synonyms) < 1:
            random_word = new_words[random.randint(0, len(new_words) - 1)]
            synonyms = EDAGenerator._get_synonyms(random_word)
            counter += 1
            if counter >= 10:
                return
        random_synonym = synonyms[0]
        random_idx = random.randint(0, len(new_words) - 1)
        new_words.insert(random_idx, random_synonym)

    @staticmethod
    def _random_insertion(words, n):
        """ Randomly insert n words into the sentence
        """
        new_words = words.copy()
        for _ in range(n):
            EDAGenerator._add_word(new_words)
        return new_words

    def generate(self, sentence):
        sentence = self._get_only_chars(sentence)
        words = sentence.split(' ')
        words = [word for word in words if word is not '']
        num_words = len(words)

        augmented_sentences = []
        num_new_per_technique = int(self.num_aug / 4) + 1
        n_sr = max(1, int(self.alpha_sr * num_words))
        n_ri = max(1, int(self.alpha_ri * num_words))
        n_rs = max(1, int(self.alpha_rs * num_words))

        # sr
        for _ in range(num_new_per_technique):
            a_words = self._synonym_replacement(words, n_sr)
            augmented_sentences.append(' '.join(a_words))

        # ri
        for _ in range(num_new_per_technique):
            a_words = self._random_insertion(words, n_ri)
            augmented_sentences.append(' '.join(a_words))

        # rs
        for _ in range(num_new_per_technique):
            a_words = self._random_swap(words, n_rs)
            augmented_sentences.append(' '.join(a_words))

        # rd
        for _ in range(num_new_per_technique):
            a_words = self._random_deletion(words, self.p_rd)
            augmented_sentences.append(' '.join(a_words))

        augmented_sentences = [self._get_only_chars(sentence) for sentence in augmented_sentences]
        shuffle(augmented_sentences)

        # trim so that we have the desired number of augmented sentences
        if self.num_aug >= 1:
            augmented_sentences = augmented_sentences[:self.num_aug]
        else:
            keep_prob = self.num_aug / len(augmented_sentences)
            augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

        # append the original sentence
        augmented_sentences.append(sentence)

        return augmented_sentences

    def batch_generate(self, sentences):
        results = dict()
        for sentence in tqdm(sentences):
            results[sentence] = self.generate(sentence)

        return results
