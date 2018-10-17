from flask import session
import datetime
import uuid
from src.models.blog import Blog
from src.common.database import Database


class User(object):
    #for login,register,create new post etc

    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

   
    # purpose of the class methods are to set or get the details (status) of the class
   #classmethod must have a reference to a class object as the first parameter, whereas staticmethod can have no parameters at all.
    @classmethod
    #while getting an email we wont have object at that time ,we need to find user first,hence we use cls
    def get_by_email(cls,email):
        data = Database.find_one("users",{"email":email})
        if data is not None:
            # cls is an object that holds the class itself, not an instance of the class.
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            # cls is an object that holds the class itself, not an instance of the class.
            return cls(**data)
        
        
    @staticmethod
    def login_valid(email,password):
        #User.login_valid("omii@123.com","1234")
        #Check whether user's email matches the password they sent us
        #create user object 
        user = User.get_by_email(email)
        if user is not None:
            # Check the password
            return user.password == password
        return False #else False
    
    #@staticmethod
    @classmethod
    def register(cls,email,password):
        #if user exist the fail ,else create
        #user = User.get_by_email(email)
        user = cls.get_by_email(email)
        if user is None:
            #User doesnt exist,so we can create it
            #new_user = User(email,password)
            #we are using 'User' in User class itself ,so rather make it classmethod
            new_user = cls(email,password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            #User Exists :(
            return False #need to show user message that user already exists

    @staticmethod
    def login(user_email):
        #since cookies can be modified manually,instead of storing email in cookies ,we will store
        #login email and password in server.Unlike a Cookie, Session data is stored on server in our database.
        #Login_valid has already been called 
        session['email'] = user_email
    
    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self,title,description):
        #author, title, description,author_id
        blog = Blog(author=self.email,
                    title = title,
                    description = description,
                    author_id = self._id)
        
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id,title, content, date=datetime.datetime.utcnow()):
        #title, content, date=datetime.datetime.utcnow()
        blog = Blog.from_mongo(blog_id) #to find blog in which new post will be created
        blog.new_post(title = title,
                    content = content,
                    date = date)

    def json(self):
        return{
            "email" : self.email,
            "_id" : self._id,
            "password" : self.password #needs to be encrypted later 
        }
    
    def save_to_mongo(self):
        Database.insert("users",self.json())
