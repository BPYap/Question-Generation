import os

from annoy import AnnoyIndex
from tqdm.auto import tqdm

from .util import file

_BATCH_SIZE = 20000
_N_TREES = 10


class Corpus:
    """ Container for raw sentences, sentence encoder and Annoy indexer
    """

    def __init__(self, corpus_path, annoy_index_path, encoder):
        """ Initialize corpus with list of sentences

        :param corpus_path: path to corpus where each line corresponds to a single sentence
        :param annoy_index_path: path where Annoy index will be/is saved
        :param encoder: encoder object inherited from BaseEncoder class
        """
        self.target_sentences = file.read_file(corpus_path, unique=True)
        self.encoder = encoder
        self.annoy_index = self._build_annoy_index(annoy_index_path)

    def _build_annoy_index(self, annoy_index_path):
        annoy_index = AnnoyIndex(self.encoder.dimension, 'angular')

        if os.path.exists(annoy_index_path):
            print(f"Loading Annoy index from {annoy_index_path}...")
            annoy_index.load(annoy_index_path, prefault=True)
        else:
            print("Building Annoy index...")
            annoy_index.on_disk_build(annoy_index_path)

            for starting_index in tqdm(range(0, len(self.target_sentences), _BATCH_SIZE)):
                target_sentences = self.target_sentences[starting_index: starting_index + _BATCH_SIZE]
                target_vectors = self.encoder.get_vectors(target_sentences)
                for i, vector in enumerate(target_vectors, start=starting_index):
                    annoy_index.add_item(i, vector)

            annoy_index.build(_N_TREES)

        return annoy_index

    def get_most_similar_sentence(self, sentence, exclude_self=True, threshold=0):
        """ Return the most similar sentence (in terms of cosine similarity) from corpus given an input sentence.
        If threshold is specified, only return the most similar sentence if its cosine similarity score
        exceed the threshold value, otherwise return None

        :param sentence: input sentence
        :param exclude_self: if True, return the second most similar sentence if the most similar sentence is the same
                             as input sentence
        :param threshold: cosine similarity threshold for the returned sentence

        :return: most similar sentence if cosine similarity exceeds threshold value else return None
        """
        if self.annoy_index is None:
            raise RuntimeError("Annoy index not found!")

        vector = self.encoder.get_vector(sentence)
        most_similar_index, distance = self.annoy_index.get_nns_by_vector(vector, 2, include_distances=True)

        most_similar_sentence = self.target_sentences[most_similar_index[0]]
        cosine_similarity_score = 0.5 * (2 - distance[0] ** 2)
        if most_similar_sentence == sentence and exclude_self:
            most_similar_sentence = self.target_sentences[most_similar_index[1]]
            cosine_similarity_score = 0.5 * (2 - distance[1] ** 2)

        return most_similar_sentence if cosine_similarity_score >= threshold else None
