import uuid
from src.common.database import Database #put __init__.py in subdirectory to include files from subdirectory
import datetime


class Post(object):  # passing object as parameter is like "extend" using Postin app.py
    #we can only have default parameter at end
    #try assigning default value to content and see all preceding it gives error
    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        #to give id automatically incase id was not assigned,as combination of string and int
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='posts', data=self.json())

    def json(self):
        return{
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    # purpose of the class methods are to set or get the details (status) of the class
    #classmethod must have a reference to a class object as the first parameter, whereas staticmethod can have no parameters at all.
    @classmethod
    #since it is class method ,like instance method it doesnt have self ,it has cls
    def from_mongo(cls, id):
        #Post.from_mongo('123')
        post_data = Database.find_one(collection='posts', query={'_id': id})
        '''         return cls(blog_id=post_data['blog_id'],
                   title=post_data['title'],
                   content=post_data['content'],
                   author=post_data['author'],
                   created_date=post_data['created_date'],
                   _id=post_data['_id']) '''
        #similar as
        # cls is an object that holds the class itself, not an instance of the class.
        return cls(**post_data)

                  

    @staticmethod  
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]
