import numpy as np
from scipy.spatial import distance
from tqdm import tqdm


class Builder:
    def __init__(self, src_path, dest_path, output_path):
        self.src_sentences = self._read_file(src_path)
        self.dest_sentences = self._read_file(dest_path)
        self.output_path = output_path

        self.encoder = None

    def set_encoder(self, encoder):
        self.encoder = encoder

    def generate_parallel_corpus(self):
        print("Initializing...")
        dest_vectors = self.encoder.get_vectors(self.dest_sentences)

        print("Generating parallel corpus...")
        parallel_corpus = dict()
        for src_sentence in tqdm(self.src_sentences):
            parallel_corpus[src_sentence] = self._get_most_similar_dest(src_sentence, dest_vectors)

        self._write_file(self.output_path, parallel_corpus)

    def _get_most_similar_dest(self, sentence, dest_vectors):
        vector = self.encoder.get_vector(sentence)
        distances = distance.cdist(np.reshape(vector, (1, -1)), dest_vectors, 'cosine')[0]
        most_similar_index = np.argmin(distances)

        return self.dest_sentences[most_similar_index]

    @staticmethod
    def _read_file(path):
        print(f"Reading from {path}...")
        sentences = set()
        with open(path, 'r', encoding='utf-8') as f:
            for line in iter(f.readline, ''):
                line = line.strip()
                if len(line) == 0 or line in sentences:
                    continue
                else:
                    sentences.add(line)

        print(f"Successfully read {len(sentences)} sentences from {path}")
        return list(sentences)

    @staticmethod
    def _write_file(path, parallel_corpus):
        print(f"Writing {len(parallel_corpus)} lines to {path}")
        with open(path, "w", encoding='utf-8') as f:
            for src_sentence, dest_sentence in tqdm(parallel_corpus.items()):
                f.write(f"{src_sentence}|||{dest_sentence}\n")
