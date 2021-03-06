import motor.motor_asyncio

from api.configs import app_configs


class MongoEngine(object):
    """Mongo client"""

    _instance = None

    def __new__(cls):
        if MongoEngine._instance is None:
            extras = {}
            if app_configs.MONGO_CAFILE:
                extras = {"tls": True, "tlsCAFile": app_configs.MONGO_CAFILE}
            client = motor.motor_asyncio.AsyncIOMotorClient(
                app_configs.ENGINE_URI, **extras
            )
            MongoEngine._instance = client[app_configs.ENGINE_DB_NAME]
        return MongoEngine._instance


db = MongoEngine()
