class BlogPost:
    def __init__(self):
        self.date = None
        self.body = None
        self.user_id = None
    
    @classmethod
    def from_elastic_result(cls, result):
        post = cls()
        post.date = result['_source']['post_date']
        post.body = result['_source']['post_text']
        post.user_id = result['_source']['user_id']

        return post
