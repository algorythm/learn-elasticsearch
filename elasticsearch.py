from requests import Session

class ElasticError(Exception):
    pass

class Elasticsearch:
    def __init__(self, host="127.0.0.1", port="9200", ssl=False):
        self.s = Session()

        self.base_url = f"http://{host}:{port}"
        if ssl==True:
            self.base_url = self.base_url.replace("http://", "https://")
    
    def create_mapping(self, name, mappings):
        # map_obj = { "mappings": mappings}

        # map_name = list(mappings["mappings"].keys())[0]
        # if self.mapping_exist(name, map_name):
        #     raise ElasticError(f"Mapping '{map_name}' or index '{name}' already exist.")

        res = self.s.put(f"{self.base_url}/{name}", json=mappings)

        if (res.status_code != 200):
            raise ElasticError(f"Failed to create mappings. Error from server: {res.text}")
        
        resjson = res.json()

        if (resjson["acknowledged"] != True):
            raise ElasticError(f"Something went wrong when creating the mapping: {resjson}")
    
    def get_indices(self):
        res = self.s.get(f"{self.base_url}/_cat/indices")

        if res.status_code != 200:
            raise ElasticError(f"Could not get indices: {res.text}")

        indices = []

        for idx in res.text.splitlines():
            indices.append(idx.split(" ")[2])

        return indices
    
    def clear_indices(self):
        indices = self.get_indices()
        for index in indices[1:]:
            print("Deleting index", index)
            self.delete_index(index)
    def clear_documents(self, index, mapping):
        if not self.mapping_exist(index, mapping):
            raise ElasticError(f"index '{index}' or mapping '{mapping}' does not exist.")
        docs = self.search(index, mapping)["hits"]["hits"]

        for doc in docs:
            deleted_doc = self.delete_document(index, mapping, doc['_id'])
            print(f"Deleted {deleted_doc['_type']} '{deleted_doc['_id']}' from '{deleted_doc['_index']}'")
    
    def delete_document(self, index, mapping, doc_id):
        if not self.mapping_exist(index, mapping):
            raise ElasticError(f"index '{index}' or mapping '{mapping}' does not exist.")
        res = self.s.delete(f"{self.base_url}/{index}/{mapping}/{doc_id}")

        if res.status_code != 200:
            raise ElasticError(f"Could not delete document '{doc_id}': {res.text}")
        
        return res.json()
    
    def delete_index(self, index):
        if not self.index_exist(index):
            raise ElasticError(f"index '{index}' does not exist.'")
        
        res = self.s.delete(f"{self.base_url}/{index}")

        if res.status_code != 200:
            raise ElasticError(f"Could not delete index '{index}': {res.text}")
        
        return res.json()

    def index_exist(self, name):
        res = self.s.head(f"{self.base_url}/{name}")
        
        if res.text != "":
            print(res.text)
        
        return res.status_code == 200
    def mapping_exist(self, index, name):
        if not self.index_exist(index):
            return False
        
        res = self.s.head(f"{self.base_url}/{index}/_mapping/{name}")

        if res.text != "":
            print(res.text)
        
        return res.status_code == 200
    
    def create_document(self, index, mapping, document):
        if not self.mapping_exist(index, mapping):
            raise ElasticError(f"index '{index}' or mapping '{mapping}' does not exist.")
        
        res = self.s.post(f"{self.base_url}/{index}/{mapping}", json=document)

        if res.status_code != 201:
            raise ElasticError(f"Could not create document: {res.text}")
        
        document = res.json()

        return document

    def get(self, index, mapping):
        return self.search(index, mapping, query=None)
    
    def search(self, index, mapping, query=None):
        if not self.mapping_exist(index, mapping):
            raise ElasticError(f"index '{index}' or mapping '{mapping}' does not exist.")

        url = f"{self.base_url}/{index}/{mapping}/_search"

        if query == None:
            query = {
                "query": {
                    "match_all": {}
                },
                "size": 100
            }
        elif isinstance(query, str):
            query = {
                "query": {
                    "match_phrase": {
                        "post_text": {
                            "query": query,
                            "slop": 3
                        },
                    },
                }
            }
        
        if isinstance(query, str):
            res = self.s.get(url)
        elif not isinstance(query, str):
            res = self.s.get(url, json=query)

        if res.status_code != 200:
            raise ElasticError(f"Failed to search: {res.text}")
        
        return res.json()
            