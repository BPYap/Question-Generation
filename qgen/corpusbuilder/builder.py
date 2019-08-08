import numpy as np
from scipy.spatial import distance

from ..util import nlp


class Builder:
    def __init__(self, tgt_path):
        """ Initialize parallel corpus builder

        :param tgt_path: path to target corpus
        """
        self.tgt_sentences = self._read_unique_lines(tgt_path)

        self.encoder = None
        self.target_vectors = None

    def set_encoder(self, encoder):
        self.encoder = encoder

    def get_most_similar_target(self, sentence, threshold=0):
        """ Return the most similar target sentence (in terms of cosine similarity) to the input sentence.
        If threshold is specified, only return the most similar sentence if its cosine similarity score
        exceed the threshold value, else return None

        :param sentence: input sentence
        :param threshold: cosine similarity threshold for the returned sentence

        :return: most similar sentence if cosine similarity exceeds threshold value else return None
        """
        if self.target_vectors is None:
            print("Initializing target vectors...")
            self.target_vectors = self.encoder.get_vectors(self.tgt_sentences)

        vector = self.encoder.get_vector(sentence)
        distances = distance.cdist(np.reshape(vector, (1, -1)), self.target_vectors, 'cosine')[0]
        most_similar_index = np.argmin(distances)
        cosine_similarity_score = 1 - distances[most_similar_index]

        return self.tgt_sentences[most_similar_index] if cosine_similarity_score >= threshold else None

    def get_refined_target(self, src, current_tgt, candidate_tgt):
        """ Refine a pair of pseudo-parallel sentences.

        :param src: source sentence
        :param current_tgt: target sentence currently matched with `src`
        :param candidate_tgt: candidate sentence to replace `current_tgt`

        :return refined target sentence
        """
        current_wmd = nlp.get_word_mover_dist(src, current_tgt)
        candidate_wmd = nlp.get_word_mover_dist(src, candidate_tgt)

        new_target, new_target_wmd = (current_tgt, current_wmd) if current_wmd < candidate_wmd \
            else (candidate_tgt, candidate_wmd)

        most_similar_original = self.get_most_similar_target(new_target)
        original_wmd = nlp.get_word_mover_dist(src, most_similar_original)

        return new_target if new_target_wmd < original_wmd else most_similar_original

    @staticmethod
    def _read_unique_lines(path):
        print(f"Reading from {path}...")
        lines = set()
        with open(path, 'r', encoding='utf-8') as f:
            for line in iter(f.readline, ''):
                line = line.strip()
                if len(line) == 0 or line in lines:
                    continue
                else:
                    lines.add(line)

        print(f"Successfully read {len(lines)} unique lines from {path}")
        return list(lines)
