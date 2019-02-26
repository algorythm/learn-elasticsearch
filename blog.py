from elasticsearch import ElasticError, Elasticsearch
from datetime import datetime
from blog_post import BlogPost

class Blog():
    def __init__(self, blog_name: str, elasticsearch: Elasticsearch):
        self.es = elasticsearch
        self.name = blog_name
        self.post_type = "post"
    
    def remove(self):
        try:
            self.es.delete_index(self.name)
        except ElasticError as e:
            print("Failed to remove blog:", e)
    def clear_all_posts(self):
        self.es.clear_documents(self.name, self.post_type)

    def ensure_created(self, synonyms: list):
        post_mapping = {
            self.post_type: {
                "properties": {
                    "user_id": {
                        "type": "integer"
                    },
                    "post_text": {
                        "type": "text",
                        "analyzer": "english"
                    },
                    "post_date": {
                        "type": "date",
                        "format": "YYYY-MM-DD"
                    }
                }
            }
        }
        settings = {
            "index": {
                "number_of_shards": 1
            },
            "analysis": {
                "filter": {
                    "blog_synonyms": {
                        "type": "synonym",
                        "synonyms": []
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    }
                }, 
                "analyzer": {
                    "english": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "blog_synonyms",
                            "english_stemmer"
                        ]
                    }
                }
            }
        }

        settings["analysis"]["filter"]["blog_synonyms"]["synonyms"] = synonyms

        mappings = { 
            "mappings": post_mapping,
            "settings": settings
        }

        self.es.create_mapping(self.name, mappings)

    def create_post(self, user_id, post, date=None):
        if date == None:
            date = datetime.now().isoformat()
        
        post = {
            "post_date": date,
            "post_text": post,
            "user_id": user_id
        }

        created_post = self.es.create_document(self.name, self.post_type, post)

        return created_post
    
    # def get_posts(self, search=None, query=None):
    #     res = self.es.search(self.name, self.post_type, search, query)

    #     posts = res["hits"]["hits"]

    #     return posts

    def get_posts(self):
        res = self.es.get(self.name, self.post_type)

        posts = []
        for hit in res["hits"]["hits"]:
            posts.append(BlogPost.from_elastic_result(hit))

        return posts

    def search(self, query=None):
        res = self.es.search(self.name, self.post_type, query)

        posts = []
        for hit in res["hits"]["hits"]:
            posts.append(BlogPost.from_elastic_result(hit))

        return posts
    
        