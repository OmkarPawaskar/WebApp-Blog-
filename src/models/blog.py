import datetime
import uuid
from src.common.database import Database
from src.models.post import Post


class Blog(object):
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.title = title
        self.description = description
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'author_id': self.author_id,
            '_id': self._id
        }

    # purpose of the class methods are to set or get the details (status) of the class
    #classmethod must have a reference to a class object as the first parameter, whereas staticmethod can have no parameters at all.

    @classmethod
    #returns object of type post instead of data
    def from_mongo(cls, _id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': _id})
        '''      return cls(author=blog_data['author'],
                   title=blog_data['title'],
                   description=blog_data['description'],
                   author_id = blog_data['author_id'],
                   _id=blog_data['_id'])
 '''  # similar as
        return cls(**blog_data)  # cls is an object that holds the class itself, not an instance of the class.

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]
