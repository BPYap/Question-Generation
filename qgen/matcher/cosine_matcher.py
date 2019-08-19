import os

from annoy import AnnoyIndex
from tqdm.auto import tqdm

from ..util import file, nlp

_BATCH_SIZE = 20000
_N_TREES = 10


class CosineSimilarityMatcher:
    """ Match sentence with given target sentences based on cosine similarity of sentence embeddings
    """

    def __init__(self, target_path, annoy_index_path, encoder):
        """ Initialize matcher with list of target sentences

        :param target_path: path to target corpus
        :param annoy_index_path: path to store index built by annoy library
        :param encoder: encoder for the computation of sentence embeddings
        """
        self.target_sentences = file.read_file(target_path, unique=True)
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

    def get_most_similar_target(self, sentence, threshold=0):
        """ Return the most similar target sentence (in terms of cosine similarity) to the input sentence.
        If threshold is specified, only return the most similar sentence if its cosine similarity score
        exceed the threshold value, else return None

        :param sentence: input sentence
        :param threshold: cosine similarity threshold for the returned sentence

        :return: most similar sentence if cosine similarity exceeds threshold value else return None
        """
        if self.annoy_index is None:
            raise RuntimeError("Annoy index not found!")

        vector = self.encoder.get_vector(sentence)
        most_similar_index, distance = self.annoy_index.get_nns_by_vector(vector, 1, include_distances=True)
        cosine_similarity_score = 0.5 * (2 - distance[0] ** 2)

        return self.target_sentences[most_similar_index[0]] if cosine_similarity_score >= threshold else None

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
