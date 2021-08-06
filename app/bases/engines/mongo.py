from pymongo import MongoClient
from django.conf import settings


class MongoClient(object):

    _instance = None

    def __new__(cls):
        if MongoClient._instance is None:
            client = MongoClient(settings.ENGINE_CONFIG)
            MongoClient._instance = client[ENGINE_DATABASE]
        return MongoClient._instance


db = MongoClient()
