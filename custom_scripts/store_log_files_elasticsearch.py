from typing import List
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def store_log_files_elasticsearch(data_rows: List[dict], index="log_database") -> str:
    es = Elasticsearch("http://elasticsearch:9200")

    if not es.ping():
        raise ConnectionError("Elasticsearch is not reachable.")

    #make anything wildcard *searchable* except timestamp
    index_mapping = {
        "dynamic_templates": [
            {
                "non_timestamp_as_wildcard": {
                    "match": "*",
                    "unmatch": "timestamp",
                    # Omit "match_mapping_type": "string" if you want integers/booleans
                    # (e.g. status: 404) to also be converted to wildcard strings.
                    "mapping": {
                        "type": "wildcard"  # Highly optimized for leading/trailing wildcards in logs (ES 7.9+)
                    }
                }
            }
        ],
        "properties": {
            "timestamp": {
                "type": "date",
                "format": (
                    "strict_date_optional_time||epoch_millis||"
                    "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm:ss.SSS"
                )
            }
        }
    }
    if not es.indices.exists(index=index):
        es.indices.create(
            index=index,
            mappings=index_mapping,
        )

    # Prepare bulk action generator
    actions = [
        {
            "_index": index,
            "_source": doc
        }
        for doc in data_rows
    ]

    # Execute bulk indexing
    success, errors = bulk(es, actions, raise_on_error=False, refresh="wait_for",)

    return f"{success} entries successfully stored, {len(errors)} entries failed"