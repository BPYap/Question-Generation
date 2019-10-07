import argparse
import json
import os
from collections import defaultdict

from qgen.encoder.universal_sentence_encoder import USEEncoder
from qgen.generator import FPMGenerator, SymSubGenerator, IMTGenerator, ZeroShotGenerator, EDAGenerator

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

AQA_PATH = os.path.join(ROOT_PATH, 'active-qa')
AQA_CONFIG_PATH = os.path.join(ROOT_PATH, 'config/aqa.json')
AQA_MODEL_PATH = os.path.join(ROOT_PATH, 'model/pretrained/active-qa/translate.ckpt-1460356')
AQA_RL_MODEL_PATH = os.path.join(ROOT_PATH, 'model/pretrained/active-qa/translate.ckpt-6156696')
# IMT_PATH = os.path.join(ROOT_PATH, 'model/onmt_model_step_15000.pt')
ONMT_PATH = os.path.join(ROOT_PATH, 'OpenNMT-py')
USE_PATH = os.path.join(ROOT_PATH, 'model/pretrained/universal_sentence_encoder')

fpm = None
symsub = None
hybrid = None
imt = None
zeroshot = None
zeroshot_rl = None
eda = None


class FPMSymSub:
    def __init__(self, fpm_generator, symsub_generator):
        self.fpm = fpm_generator
        self.symsub = symsub_generator
        self.name = "Hybrid mode (FPM + SymSub)"

    def batch_generate(self, sentences):
        print("Generating with FPM...")
        temp1 = self.symsub.batch_generate(sentences)
        print("Generating with SymSub...")
        temp2 = self.fpm.batch_generate([s for k, v in temp1.items() for s in [k] + v])

        results = defaultdict(list)
        for key, values in temp1.items():
            results[key].extend(temp2[key])
            for value in values:
                results[key].extend(temp2[value])

        return results


def main(method, input_path, output_path, batch_size=2500):
    if method == 'fpm':
        generator = FPMGenerator()
    elif method == 'symsub':
        generator = SymSubGenerator(USEEncoder(USE_PATH))
    elif method == 'hybrid':
        generator = FPMSymSub(FPMGenerator(), SymSubGenerator(USEEncoder(USE_PATH)))
    # elif method == 'imt':
    #     generator = IMTGenerator(ONMT_PATH, IMT_PATH, n_best=5)
    elif method == 'zeroshot':
        generator = ZeroShotGenerator(AQA_PATH, AQA_CONFIG_PATH, AQA_MODEL_PATH)
    elif method == 'zeroshot-rl':
        generator = ZeroShotGenerator(AQA_PATH, AQA_CONFIG_PATH, AQA_RL_MODEL_PATH)
    elif method == 'eda':
        generator = EDAGenerator()
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
                        help="Question generation method."
                        # "Available option: [fpm, symsub, hybrid, imt, zeroshot, zeroshot-rl, eda]")
                             "Available option: [fpm, symsub, hybrid, zeroshot, zeroshot-rl, eda]")
    parser.add_argument("--input_path",
                        help="Path to input file in plain text, each question is separated by newline")
    parser.add_argument("--output_path",
                        help="Path to output file in json format, each question maps to a list of generated questions")

    args = parser.parse_args()

    main(args.method, args.input_path, args.output_path)
