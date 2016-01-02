from pymongo import MongoClient
from crawler import settings


class MongoDBClient(object):
    def __init__(self, collection):
        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_DBNAME]
        self.collection = db[collection]
