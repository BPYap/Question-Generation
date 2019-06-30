import argparse
import json
from collections import defaultdict

from qgen.util.file import read_file


def main(src_path, translated_path, output_path, num_sentence):
    src_lines = read_file(src_path)
    translated_lines = read_file(translated_path)
    formatted = defaultdict(list)

    for src in src_lines:
        for i in range(num_sentence):
            formatted[src].append(translated_lines.pop(0))

    with open(output_path, 'w') as f:
        json.dump(formatted, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--src_path")
    parser.add_argument("--translated_path")
    parser.add_argument("--json_path")
    parser.add_argument("--num_sent")
    args = parser.parse_args()

    main(args.src_path, args.translated_path, args.json_path, int(args.num_sent))
