from api import configs
import motor.motor_asyncio


class MongoEngine(object):

    _instance = None

    def __new__(cls):
        if MongoEngine._instance is None:
            client = motor.motor_asyncio.AsyncIOMotorClient(configs.ENGINE_URI)
            MongoEngine._instance = client[configs.ENGINE_DB_NAME]
        return MongoEngine._instance

db = MongoEngine()
