import argparse
import codecs
import os

import onmt.opts as opts
from onmt.translate.translator import build_translator
from onmt.utils.parse import ArgumentParser


def _run(model_path, n_best=5):
    onmt_parser = ArgumentParser()
    opts.translate_opts(onmt_parser)
    opt = onmt_parser.parse_args([f"--model={model_path}", "--src=''", f"--n_best={n_best}"])

    translator = build_translator(opt, report_score=False, out_file=codecs.open(os.devnull, "w", "utf-8"))

    while True:
        input_sentence = input("Enter a sentence/question: ")
        _, rewrites = translator.translate([input_sentence], batch_size=1)

        print("\nTop 5 rewrites:")
        for index, rewrite in enumerate(rewrites[0]):
            print(f"{index + 1}. {rewrite}")
        print('=' * 100)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path")

    _run(parser.parse_args().model_path)
