from api import configs
from api.services.node_mongo import ServiceNodeMongo

ENGINE_TYPES = {"MONGO": ServiceNodeMongo}

service_node = ENGINE_TYPES[configs.ENGINE_NAME]

__all__ = ("service_node",)
