from elasticsearch import Elasticsearch

def clear_database(index: str = "log_database"):
    es = Elasticsearch("http://elasticsearch:9200")

    if not es.ping():
        raise ConnectionError("Elasticsearch is not responding")

    # delete index
    es.indices.delete(index=index, ignore_unavailable=True)

    # simply return, no return required for simplicity
    return


if __name__ == "__main__":
     clear_database()