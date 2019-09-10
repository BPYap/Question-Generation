import codecs
import importlib
import os
import sys

from .base import BaseGenerator

_BATCH_SIZE = 16


class IMTGenerator(BaseGenerator):
    """ Generate questions using text style transfer model trained on iterative matching and translation
        method (Reference: https://arxiv.org/abs/1901.11333) """

    def __init__(self, onmt_path, model_path, n_best):
        """
        :param onmt_path: path to OpenNMT toolkit directory
        :param model_path: path to trained model
        :param n_best: number of rewrites to generate for each sentence
        """
        super().__init__("IMT Style Transfer Model")

        self.n_best = n_best
        self.translator = self._get_translator(onmt_path, model_path, n_best)

    @staticmethod
    def _get_translator(onmt_path, model_path, n_best):
        sys.path.insert(0, onmt_path)
        opts = importlib.import_module('onmt.opts')
        build_translator = importlib.import_module('onmt.translate.translator').build_translator
        argument_parser = importlib.import_module('onmt.utils.parse').ArgumentParser

        onmt_parser = argument_parser()
        opts.translate_opts(onmt_parser)
        opt = onmt_parser.parse_args([f"--model={model_path}", "--src=''", f"--n_best={n_best}", "--replace_unk"])

        return build_translator(opt, report_score=False, out_file=codecs.open(os.devnull, "w", "utf-8"))

    def generate(self, sentence):
        return list(self.batch_generate([sentence]).values())[0]

    def batch_generate(self, sentences):
        _, translation_result = self.translator.translate(sentences, batch_size=_BATCH_SIZE)

        results = dict()
        for i, rewrites in enumerate(translation_result):
            results[sentences[i]] = rewrites

        return results
