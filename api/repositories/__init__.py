from api.configs import app_configs
from api.features.config import get_feature_repository
from api.repositories.mongo import BaseRepository
from api.repositories.mongo import MongoRepository


REPOSITORY_TYPES = {"MONGO": (MongoRepository, BaseRepository)}
Repository, Base = REPOSITORY_TYPES[app_configs.ENGINE_NAME]


def repository_from_feature():
    """Return the `repository` according to the available repository.

    Returns:
        Repository: repository available.
    """
    feature_repo = get_feature_repository()
    if feature_repo:
        return feature_repo
    return Repository
