"""
possible llm_query_dict - dsl examples
{
    "timestamp": {gte|gt": "2015-01-01", "lte|lt": "2015-01-10" },
    "severity": [INFO|WARN|ERROR]", # "", not present, or list of all of them for no delimiter
    "log_type|component|event|message|...": "contains_x"
}

{
    "timestamp": {
    "value": "2026-10-20",
    "operator": "lt|lte|gt|gte",
    },
    "severity": ["INFO", "WARN"],
    "log_type|component|event|message|...": "contains_x"
}


{
  "query": {
    "bool": {
      "must": [
        { "wildcard": { "log_type": { "value": "*x*", "case_insensitive": true } } },
        { "wildcard": { "component": { "value": "*x*", "case_insensitive": true } } },
        { "wildcard": { "event": { "value": "*x*", "case_insensitive": true } } },
        { "wildcard": { "message": { "value": "*x*", "case_insensitive": true } } }
      ],
      "filter": [
        { "terms": { "severity": ["WARN", "ERROR"] } },
        { "range": { "timestamp": { "lte": "2015-01-10" } } }
      ]
    }
  }
}
https://www.elastic.co/docs/explore-analyze/query-filter/languages/querydsl
"""


from typing import List
def build_query(llm_query_dict: dict):


    if not llm_query_dict:
        return {"query": {"match_all": {}}}
    else:
        final_query = {"query": _build_query(llm_query_dict)}

    return final_query

def _build_query(llm_query_dict: dict):
    result:dict = {"bool":{"must":[], "filter":[]}}

    for key, value in llm_query_dict.items():
            if key == "timestamp":
                if isinstance(value, dict):
                    range_dict:dict = {"range": {"timestamp": {}}}
                    for operator, date in value.items():
                        if operator not in ["gt", "lt", "gte", "lte"]:
                            raise ValueError(f"Unsupported operator: {operator}. Supported operators: 'gt', 'lt', 'gte', 'lte'")
                        else:
                            range_dict["range"]["timestamp"][operator] = date
                    result["bool"]["filter"].append(range_dict)
                else:
                    raise TypeError(f"Expected a dict but found {type(value)}")

            elif key == "severity":
                if isinstance(value, list):
                    valid_items:list = []
                    for item in value:
                        item = item.upper()
                        if item in ["INFO", "WARN", "ERROR"]:
                            valid_items.append(item)
                        else:
                            raise ValueError(f"Unsupported severity: {item}. Supported severity options: 'INFO', 'WARN', 'ERROR'")
                    result["bool"]["filter"].append({"terms": {"severity": valid_items}})

                else:
                    raise TypeError(f"Expected a list but found {type(value)}")

            else:
                if isinstance(value, str):
                    result["bool"]["must"].append({"wildcard": {_escape_value(key): _escape_value(value)}})
                    #TODO ensure wildcards are injection free - the keys should be bound to an allowlist, but for this prototype its fine
                else:
                    raise TypeError(f"Expected a str but found {type(value)}")

    return result

def _escape_value(input) -> str:
    raw_val = str(input)

    # 1. Check for leading/trailing wildcards
    has_leading_star = raw_val.startswith("*")
    has_trailing_star = raw_val.endswith("*")
    # 2. Strip boundary wildcards for escaping
    core_val = raw_val.strip("*")
    # 3. Escape dangerous internal characters
    escaped_core = core_val.replace("\\", "\\\\").replace("*", "\\*").replace("?", "\\?")
    # 4. Truncate string if too long
    escaped_core = escaped_core[:100]
    # 5. Reconstruct value
    prefix = "*" if has_leading_star else ""
    suffix = "*" if has_trailing_star else ""
    escaped_value = f"{prefix}{escaped_core}{suffix}"

    return escaped_value