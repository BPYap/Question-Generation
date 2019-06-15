from qgen.util.config import load_yaml_config
from qgen.util.file import read_file, write_file, delete_file, split_file
from qgen.util.nlp import tokenize

if __name__ == '__main__':
    yaml_config = load_yaml_config()

    src_full_path = yaml_config['source_full_path']
    tgt_full_path = yaml_config['target_full_path']

    src_train_path = yaml_config['source_train_path']
    tgt_train_path = yaml_config['target_train_path']

    src_valid_path = yaml_config['source_validation_path']
    tgt_valid_path = yaml_config['target_validation_path']
    validation_ratio = float(yaml_config['validation_ratio'])

    src_test_path = yaml_config['source_test_path']
    tgt_test_path = yaml_config['target_test_path']
    test_ratio = float(yaml_config['test_ratio'])

    # 1. Tokenize sentences and write to temp file
    src_temp_path = "src_temp.txt"
    src_lines = read_file(src_full_path)
    write_file([" ".join(tokenize(line)) for line in src_lines], src_temp_path)

    tgt_temp_path = "tgt_temp.txt"
    tgt_lines = read_file(tgt_full_path)
    write_file([" ".join(tokenize(line)) for line in tgt_lines], tgt_temp_path)

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
