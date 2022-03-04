from api.configs import app_configs
from api.services.node_mongo import ServiceNodeMongo

ENGINE_TYPES = {"MONGO": ServiceNodeMongo}

service_node = ENGINE_TYPES[app_configs.ENGINE_NAME]

__all__ = ("service_node",)
