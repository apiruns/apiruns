from api.configs import app_configs
from api.engines.mongo import db as db_mongo

ENGINE_TYPES = {"MONGO": db_mongo}

db = ENGINE_TYPES[app_configs.ENGINE_NAME.upper()]
