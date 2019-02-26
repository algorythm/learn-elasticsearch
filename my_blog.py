from elasticsearch import Elasticsearch
from blog import Blog
import sys

es = Elasticsearch(port = 9201)
my_blog = Blog("my_blog", es)
my_blog.remove()

print("Make sure the blog is created.")
my_blog.ensure_created(["dane,denmark"])

def create_the_stuff():
    my_blog.clear_all_posts()
    my_blog.create_post(1, "This is my first blog post!", "2019-02-25")
    my_blog.create_post(2, "This is another totally real blog post.", "2019-02-15")
    my_blog.create_post(1, "I will be writing a lot of bullshit posts for demonstation.", "2019-01-01")
    my_blog.create_post(1, "There are only two people writing shit on this post.", "2019-02-13")
    my_blog.create_post(2, "What the fuck can I write useless posts in my fictive blog about?", "2019-02-22")
    my_blog.create_post(1, "This post is from the future, wow...", "2020-04-30")
    my_blog.create_post(2, "Most poeple in Denmark likes beer.", "2019-02-25")
    my_blog.create_post(2, "The vikings originates from the Danes.", "2018-12-24")
    my_blog.create_post(1, "I like most kinds of beverages.", "2019-02-14")
    my_blog.create_post(2, "This is an extremely nice ale.", "2019-02-19")
    my_blog.create_post(2, "Many people does not drink enough water, especially during summer.", "2019-01-19")
    my_blog.create_post(2, "Coffee does not count for drinking enough!", "2017-07-11")
    my_blog.create_post(1, "Java is a special kind of coffee", "2018-05-27")
    my_blog.create_post(1, "At DTU, software students start by learning Java", "2018-12-13")
    my_blog.create_post(1, "There are a huge amount of people in China", "2018-10-27")
    my_blog.create_post(2, "The company will be entering the global market", "2018-04-23")
    my_blog.create_post(3, "Welcome to my new cat blog", "2018-03-13")
    my_blog.create_post(3, "I have a lot of pets", "2018-03-16")
    my_blog.create_post(3, "Dogs are the cat's worst enemy", "2018-03-17")
    my_blog.create_post(3, "I was once bit by a dog", "2018-03-19")
    my_blog.create_post(2, "I once saw an animal get slaugtered.", "2018-07-10")

def search(q=None):
    results = my_blog.search(q)
    print(f"Found {len(results)} items matching your search.")
    for post in results:
        print(f"- {post.date}: {post.body}")
        # print(f"- {post['_source']['post_date']}: {post['_source']['post_text']}")

create_the_stuff()

import time
time.sleep(1)

print("All posts")
search()
while(True):
    s = input("Search: ")
    if s == "q":
        break
    search(s)
