from api.configs import app_configs
from api.repositories.mongo import MongoRepository

REPOSITORY_TYPES = {"MONGO": MongoRepository}

repository = REPOSITORY_TYPES[app_configs.ENGINE_NAME]
