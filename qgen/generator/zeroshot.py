import importlib
import sys

from .base import BaseGenerator


class ZeroShotGenerator(BaseGenerator):
    """ Generate questions using zero-shot neural machine translation model
        (Reference: https://arxiv.org/abs/1705.07830)"""

    def __init__(self, aqa_path, config_path, model_path):
        """
        :param aqa: path to active-qa directory
        :param model_path: path to trained model
        :param n_best: number of rewrites to generate for each sentence
        """
        super().__init__("ActiveQA Zero-shot neural machine translation model")

        self.reformulator = self._get_translator(aqa_path, config_path, model_path)

    @staticmethod
    def _get_translator(aqa_path, config_path, model_path):
        sys.path.insert(0, aqa_path)
        reformulator = importlib.import_module('px.nmt.reformulator')

        reformulator_instance = reformulator.Reformulator(
            hparams_path=config_path,
            source_prefix='<en> <2en> ',
            out_dir=model_path,
            environment_server_address='')

        return reformulator_instance

    def generate(self, sentence):
        return list(self.batch_generate([sentence]).values())[0]

    def batch_generate(self, sentences):
        reformulator_pb2 = importlib.import_module('px.proto.reformulator_pb2')
        responses = self.reformulator.reformulate(questions=sentences,
                                                  inference_mode=reformulator_pb2.ReformulatorRequest.BEAM_SEARCH)

        results = dict()
        for i, response in enumerate(responses):
            temp = []
            for j, rewrite in enumerate(response):
                temp.append(rewrite.reformulation)
            results[sentences[i]] = temp

        return results
