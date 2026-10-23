import json
import sys

from elasticsearch_query_builder import build_query
from query_elasticsearch import query_elasticsearch

def parse_json_arg(raw):
    if raw in (None, "", "None", "null"):
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw

def main():
    llm_query_json = parse_json_arg(sys.argv[1]) if len(sys.argv) > 1 else None
    try:
        llm_query_dict:dict = json.loads(llm_query_json)
    except json.JSONDecodeError:
        return print("Invalid JSON format")
    built_query = build_query(llm_query_dict)
    result = query_elasticsearch(built_query)
    return result


if __name__ == "__main__":
    result = main()
    print(result)  # !this is important since the tool will read the print!