from api.configs import app_configs
from api.features import internals
from api.features.internals.micro import models
from api.repositories.mongo import BaseRepository
from api.repositories.mongo import MongoRepository

REPOSITORY_TYPES = {"MONGO": (MongoRepository, BaseRepository)}
Repository, Base = REPOSITORY_TYPES[app_configs.ENGINE_NAME]


def repository_from_feature():
    feature = internals.features.get(internals.InternalFeature.MICRO)
    if feature.is_on:
        return models.Repository
    return Repository
