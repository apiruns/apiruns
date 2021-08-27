from api.repositories.mongo import MongoRepository
from api import configs

REPOSITORY_TYPES = {
    "MONGO": MongoRepository
}

repository = REPOSITORY_TYPES[configs.ENGINE_NAME]
