from app.api import configs
from app.api.engines.mongo import db as db_mongo

ENGINE_TYPES = {
    "MONGO": db_mongo
}

db = ENGINE_TYPES[configs.ENGINE_NAME]
