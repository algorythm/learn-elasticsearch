from elasticsearch import Elasticsearch
from blog_post import BlogPost
from blog import Blog
from time import sleep

es = Elasticsearch(port = 9201)
blog = Blog("synonym_test", es)

blog.remove()

synonyms = [
    "cat => cat, pet",
    "dog => dog, pet"
]

blog.ensure_created(synonyms)

blog.create_post(1, "My cat is awesome", "2019-02-24")
blog.create_post(1, "I once had a dog", "2019-02-25")
blog.create_post(2, "I love my awesome cat", "2019-01-13")

# Elastic search take some time to index
sleep(1) 

posts = blog.get_posts()

for post in posts:
    print(f"- {post.date}: {post.body}")

print("Searching for 'awesome cat'")
for post in blog.search("awesome cat"):
    print(f"- {post.date}: {post.body}")

print("Searching for 'cat' for user 1")
query = {
    "query": {
        "bool": {
            "must": [
                { 
                    "match_phrase": { 
                        "post_text": {
                            "query": "awesome cats",
                            "slop": 3
                        }
                    }
                }
            ],
            "filter": [
                { "term": { "user_id": 1 } }
            ]
        }
    }
}

for post in blog.search(query):
    print(f"- {post.date}: {post.body}")
