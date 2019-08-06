import os
from pathlib import Path


def get_filename(path):
    return Path(path).name


def create_folder(path):
    if os.path.exists(path):
        print(f"{path} already exists.")
    else:
        os.mkdir(path)


def read_file(path):
    print(f"Reading from {path}...")
    lines = list()
    with open(path, 'r', encoding='utf-8') as f:
        for line in iter(f.readline, ''):
            lines.append(line.strip())

    print(f"Read {len(lines)} lines from {path}")
    return list(lines)


def write_file(lines, path):
    print(f"Writing {len(lines)} lines to {path}...")
    with open(path, "w", encoding='utf-8') as f:
        for line in lines:
            f.write(f"{line}\n")


def split_file(input_path, output_path1, output_path2, split_ratio):
    lines = read_file(input_path)
    num_lines = int(len(lines) * split_ratio)
    write_file(lines[num_lines:], output_path1)
    write_file(lines[:num_lines], output_path2)


def delete_file(*paths):
    for path in paths:
        os.remove(path)
