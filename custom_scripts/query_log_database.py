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
    llm_query_dict = parse_json_arg(sys.argv[1]) if len(sys.argv) > 1 else None
    if llm_query_dict is None:
        llm_query_dict = {}
    if not isinstance(llm_query_dict, dict):
        raise ValueError("The query must be a JSON object")
    built_query = build_query(llm_query_dict)
    result = query_elasticsearch(built_query)
    return result


if __name__ == "__main__":
    try:
        result = main()
        print(json.dumps(result, ensure_ascii=False))
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)