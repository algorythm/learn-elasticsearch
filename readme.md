# Learning elasticsearch with Python

This repository is for toying around with elasticsearch. I have
played a bit with it in [another repository](https://github.com/algorythm/LaravelElasticsearch),
though in there I used a framework. Furthermore, PHP is not my
strong side, so for faster learning, I chose to develop a small
tool in python to work with elasticsearch.

## Run

To run the project, make sure to have installed python3, docker and virtualenv. Then run:

```bash
virtualenv -p python3 venv
source ./venv/bin/activate
pip install -r requirements.txt
docker run \
    --name estest \
    -p 9201:9200 \
    -e "discovery.type=single-node" \
    -d docker.elastic.co/elasticsearch/elasticsearch:6.1.0

python3 my_blog.py
python3 synonym_blog.py
```

## Information

`synonym_blog.py` is currently not working. It was an attempt to
setup one-directional synonyms, though it seemed I either did
something wrong, or elasticsearch's documentation was wrong.
Read the comments in the file for more information.
