from typing import List
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def store_log_files_elasticsearch(data_rows: List[dict]) -> str:
    es = Elasticsearch("http://elasticsearch:9200")

    if not es.ping():
        raise ConnectionError("Elasticsearch is not reachable.")

    # Prepare bulk action generator
    actions = [
        {
            "_index": "log_database",
            "_source": doc
        }
        for doc in data_rows
    ]

    # Execute bulk indexing
    success, errors = bulk(es, actions, raise_on_error=False)

    return f"{success} entries successfully stored, {len(errors)} entries failed"