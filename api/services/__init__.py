from api.configs import app_configs
from api.services.model_mongo import ServiceModelMongo

ENGINE_TYPES = {"MONGO": ServiceModelMongo}

service_model = ENGINE_TYPES[app_configs.ENGINE_NAME.upper()]

__all__ = ("service_model",)
