import argparse
import json
import os

from tqdm import tqdm

from qgen.encoder.universal_sentence_encoder import USEEncoder
from qgen.generator import FPMGenerator, SymSubGenerator, IMTGenerator, ZeroShotGenerator, EDAGenerator

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

AQA_PATH = os.path.join(ROOT_PATH, 'active-qa')
AQA_CONFIG_PATH = os.path.join(ROOT_PATH, 'config/pretrained/aqa.json')
AQA_MODEL_PATH = os.path.join(ROOT_PATH, 'model/pretrained/active-qa/translate.ckpt-1460356')
IMT_PATH = os.path.join(ROOT_PATH, 'model/yahoo-18-Aug/0-onmt_model_step_5000.pt')
ONMT_PATH = os.path.join(ROOT_PATH, 'OpenNMT-py')
USE_PATH = os.path.join(ROOT_PATH, 'model/pretrained/universal_sentence_encoder')

fpm = None
symsub = None
imt = None
zeroshot = None
eda = None


def init():
    print("Initializing...")
    global fpm, symsub, imt, zeroshot, eda

    fpm = FPMGenerator()
    symsub = SymSubGenerator(USEEncoder(USE_PATH))
    imt = IMTGenerator(ONMT_PATH, IMT_PATH, 5)
    zeroshot = ZeroShotGenerator(AQA_PATH, AQA_CONFIG_PATH, AQA_MODEL_PATH)
    eda = EDAGenerator()


def main(method, input_path, output_path):
    if method == 'fpm':
        generator = fpm
    elif method == 'symsub':
        generator = symsub
    elif method == 'imt':
        generator = imt
    elif method == 'zeroshot':
        generator = zeroshot
    elif method == 'eda':
        generator = eda
    else:
        print("Unknown method. Default to fpm generator")
        generator = fpm

    result = dict()

    line_count = 0
    with open(input_path, 'r', encoding='utf-8') as f:
        for _ in f:
            line_count += 1

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in tqdm(f, total=line_count):
            result[line] = generator.generate(line)

    print(f"Saving result to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f)

    print("Done.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--method",
                        help="Question generation method. Available option: [fpm, symsub, imt, zeroshot, eda]")
    parser.add_argument("--input_path",
                        help="Path to input file in plain text, each question is separated by newline")
    parser.add_argument("--output_path",
                        help="Path to output file in json format, each question maps to a list of generated questions")

    args = parser.parse_args()

    init()
    main(args.method, args.input_path, args.output_path)
