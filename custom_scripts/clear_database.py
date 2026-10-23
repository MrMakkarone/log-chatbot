from elasticsearch import Elasticsearch

def _clear_database(index: str = "log_database"):
    es = Elasticsearch("http://elasticsearch:9200")

    if not es.ping():
        raise ConnectionError("Elasticsearch is not responding")

    # delete and recreate index
    es.indices.delete(index=index, ignore_unset=True)
    es.indices.create(index=index)

    # simply return, no return required for simplicity
    return


if __name__ == "__main__":
     _clear_database()