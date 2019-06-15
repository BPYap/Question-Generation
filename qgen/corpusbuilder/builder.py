import numpy as np
from scipy.spatial import distance
from tqdm import tqdm

from ..util import file


class Builder:
    def __init__(self, src_path, tgt_path, src_output_path, tgt_output_path):
        """ Initialize parallel corpus builder

        :param src_path: path to corpus containing questions of particular style/tone in random order
        :param tgt_path: path to corpus containing questions of another style/tone in random order
        :param src_output_path: output path to parallel corpus generated from corpus in `src_path`
        :param tgt_output_path: output path to parallel corpus generated from corpus in `tgt_path`
        """
        self.src_sentences = self._read_unique_lines(src_path)
        self.tgt_sentences = self._read_unique_lines(tgt_path)
        self.src_output_path = src_output_path
        self.tgt_output_path = tgt_output_path

        self.encoder = None

    def set_encoder(self, encoder):
        self.encoder = encoder

    def build_parallel_corpus(self):
        """ Generate pseudo-parallel corpus based on cosine distances between source corpus and target corpus.
        Results will be saved into 2 different files (`self.src_output_path` and `self.tgt_output_path`) in which
        a line in `self.src_output_path` is "parallel"/"translated" to the same line in `self.tgt_output_path`.
        """
        print("Initializing...")
        tgt_vectors = self.encoder.get_vectors(self.tgt_sentences)

        print("Generating parallel corpus...")
        src_sentences = []
        tgt_sentences = []
        for src_sentence in tqdm(self.src_sentences):
            src_sentences.append(src_sentence)
            tgt_sentences.append(self._get_most_similar_tgt(src_sentence, tgt_vectors))

        assert len(src_sentences) == len(tgt_sentences)

        file.write_file(src_sentences, self.src_output_path)
        file.write_file(tgt_sentences, self.tgt_output_path)

    def _get_most_similar_tgt(self, sentence, tgt_vectors):
        vector = self.encoder.get_vector(sentence)
        distances = distance.cdist(np.reshape(vector, (1, -1)), tgt_vectors, 'cosine')[0]
        most_similar_index = np.argmin(distances)

        return self.tgt_sentences[most_similar_index]

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
