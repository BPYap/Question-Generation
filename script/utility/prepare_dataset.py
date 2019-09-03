import argparse

from qgen.util.file import read_file, write_file, delete_file, split_file
from qgen.util.nlp import get_spacy_model


def main(src_full_path, tgt_full_path, src_train_path, tgt_train_path, src_valid_path, tgt_valid_path, validation_ratio,
         src_test_path, tgt_test_path, test_ratio):
    # 1. Tokenize sentences and write to temp file
    nlp = get_spacy_model()
    with nlp.disable_pipes('ner'):
        src_temp_path = "src_temp.txt"
        src_lines = read_file(src_full_path)
        write_file(
            list(" ".join(tokens) for tokens in [[token.text for token in doc] for doc in nlp.pipe(src_lines)]),
            src_temp_path
        )

        tgt_temp_path = "tgt_temp.txt"
        tgt_lines = read_file(tgt_full_path)
        write_file(
            list(" ".join(tokens) for tokens in [[token.text for token in doc] for doc in nlp.pipe(tgt_lines)]),
            tgt_temp_path
        )

    # 2. Split into train, validation, test files
    src_valid_test_temp_path = "src_valid_test_temp.txt"
    split_file(src_temp_path, src_train_path, src_valid_test_temp_path, validation_ratio + test_ratio)

    tgt_valid_test_temp_path = "tgt_valid_test_temp.txt"
    split_file(tgt_temp_path, tgt_train_path, tgt_valid_test_temp_path, validation_ratio + test_ratio)

    ratio = validation_ratio / (validation_ratio + test_ratio)
    split_file(src_valid_test_temp_path, src_valid_path, src_test_path, ratio)
    split_file(tgt_valid_test_temp_path, tgt_valid_path, tgt_test_path, ratio)

    # 3. Delete temp files
    print("Cleaning up...")
    delete_file(src_temp_path, tgt_temp_path, src_valid_test_temp_path, tgt_valid_test_temp_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_src")
    parser.add_argument("--input_tgt")
    parser.add_argument("--train_src")
    parser.add_argument("--train_tgt")
    parser.add_argument("--valid_src")
    parser.add_argument("--valid_tgt")
    parser.add_argument("--validation_ratio")
    parser.add_argument("--test_src")
    parser.add_argument("--test_tgt")
    parser.add_argument("--test_ratio")
    args = parser.parse_args()

    main(args.input_src, args.input_tgt, args.train_src, args.train_tgt, args.valid_src, args.valid_tgt,
         float(args.validation_ratio), args.test_src, args.test_tgt, float(args.test_ratio))
