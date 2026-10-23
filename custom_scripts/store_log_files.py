from typing import List

from store_log_files_elasticsearch import store_log_files_elasticsearch
import json
import csv

def store_log_files(file_paths)-> str:
    try:
        file_paths = json.loads(file_paths)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: Invalid JSON. {e}")
    if not file_paths:
        raise ValueError("No files found")

    data_rows: List[dict] = []
    for file_path in file_paths:
        csv_to_dict = csv_to_dict_list(file_path)
        for row in csv_to_dict:
            data_rows.append(row)

    return store_log_files_elasticsearch(data_rows)

def csv_to_dict_list(file_path: str) -> list[dict]:
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        return list(reader)