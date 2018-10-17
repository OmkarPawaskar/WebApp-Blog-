import pymongo


class Database(object):  # passing object as parameter is like "extend" using Database in post.py
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    
    #instance method depends upon object hence we use self
    #static method:neither self (the object instance) nor  cls (the class) is implicitly passed as the first argument
    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
