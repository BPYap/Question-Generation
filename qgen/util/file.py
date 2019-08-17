import json
import os
from pathlib import Path


def get_filename(path):
    return Path(path).name


def create_folder(path):
    if os.path.exists(path):
        print(f"{path} already exists.")
    else:
        os.mkdir(path)


def read_json(path):
    with open(path, 'r') as f:
        data = json.load(f)

    return data


def read_file(path, unique_lines=False):
    print(f"Reading from {path}...")
    lines = dict()
    with open(path, 'r', encoding='utf-8') as f:
        for line in iter(f.readline, ''):
            line = line.strip()
            if (unique_lines and line not in lines) or not unique_lines:
                lines[line] = 1

    print(f"Read {len(lines)} lines from {path}")
    return list(lines.keys())


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
