from typing import List

from store_log_files_elasticsearch import store_log_files_elasticsearch
import json
import csv
import sys

def parse_json_arg(raw):
    if raw in (None, "", "None", "null"):
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def store_log_files()-> str:
    file_paths = parse_json_arg(sys.argv[1]) if len(sys.argv) > 1 else None
    if file_paths is None:
        raise ValueError("No files found")
    if not isinstance(file_paths, list):
        raise ValueError("The input must be a JSON array of file paths")

    data_rows: List[dict] = []
    for file_path in file_paths:
        csv_to_dict = csv_to_dict_list(file_path)
        data_rows.extend(csv_to_dict)

    return store_log_files_elasticsearch(data_rows)

def csv_to_dict_list(file_path: str) -> list[dict]:
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)


if __name__ == "__main__":
    print(store_log_files())
