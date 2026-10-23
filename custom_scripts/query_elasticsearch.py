from elasticsearch import Elasticsearch
#10k is max retrieval size, different approach if more is needed
def query_elasticsearch(query, index="log_database", size=10000):

    es = Elasticsearch("http://elasticsearch:9200")

    if query is None:
        raise ValueError("Missing query")

    if not es.ping():
        raise ConnectionError("Elasticsearch is not responding")

    response = es.search(index=index, body=query, size=size)
    result = []

    for hit in response['hits']['hits']:
        source = hit['_source']
        result.append(source)

    return result