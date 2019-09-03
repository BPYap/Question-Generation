import argparse
import json
import os

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
    imt = None
    zeroshot = ZeroShotGenerator(AQA_PATH, AQA_CONFIG_PATH, AQA_MODEL_PATH)
    eda = EDAGenerator()


def main(method, input_path, output_path, batch_size=2500):
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

    print(f"Generating questions via {generator.name}...")
    results = dict()
    batch_counter = 0

    def process_batch(_batch):
        if len(_batch) > 0:
            nonlocal results, batch_counter
            print(f"Processing batch #{batch_counter}...")
            results.update(generator.batch_generate(_batch))
            batch_counter += 1

    with open(input_path, 'r', encoding='utf-8') as f:
        batch_counter = 0
        batch = []
        for line in f:
            if len(line.strip()) != 0:
                batch.append(line.strip())
                if len(batch) == batch_size:
                    process_batch(batch)
                    batch = []

        process_batch(batch)

    print(f"Saving result to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f)

    num_generated = sum([len(v) for v in results.values()])
    print(f"Done. Number of questions generated: {num_generated} ({num_generated / len(results) * 100}% increases)")


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
