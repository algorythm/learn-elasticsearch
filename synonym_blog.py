"""
This script is for testing synonyms

We want to say that a
- cat is a pet
- dog is a pet

When searching for 'cat', we only want blog posts that include 'cat'.
When searching for 'dog', we only want blog posts that include 'dog'.
When searching for 'pet', we want blog posts that include 'cat' and 'dog'.

See https://www.elastic.co/guide/en/elasticsearch/guide/master/synonyms-analysis-chain.html
See https://stackoverflow.com/questions/34333486/one-way-synonym-search-in-elasticsearch
"""

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

print("All posts")
for post in posts:
    print(f"- {post.date}: {post.body}")

print("Searching for 'cat'")

for post in blog.search("cat"):
    print(f"- {post.body}")
    assert not "dog" in post.body
for post in blog.search("dog"):
    print(f"- {post.body}")
    assert not "cat" in post.body
cats = 0
dogs = 0
for post in blog.search("pet"):
    print(f"- {post.body}")
    if "cat" in post.body:
        cats += 1
    if "dog" in post.body:
        dogs += 1
assert cats > 0 and dogs > 0

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
    assert post.user_id == 1
