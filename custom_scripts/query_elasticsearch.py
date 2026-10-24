import sys

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

#test database query. Dont forget to change to http://localhost:9200 instead of http://elasticsearch:9200
#if __name__ == "__main__":
#    query_dict:dict = {'query': {'bool': {'must': [{'wildcard': {'username': 'a.jones'}}], 'filter': [{'range': {'timestamp': {'gte': '2026-10-20 01:30:00', 'lte': '2026-10-20 11:30:00'}}}, {'terms': {'severity': ['ERROR', 'WARN']}}]}}}
#
#    result = query_elasticsearch(query = query_dict)
#    print(result)