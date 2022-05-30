from typing import List
from typing import Union

from dacite import from_dict

from api.configs import app_configs
from api.datastructures import Model
from api.engines import db


class BaseRepository:

    main_model = app_configs.MODEL_ADMIN_NAME
    main_field = app_configs.IDENTIFIER_ID
    client = db

    @staticmethod
    async def create_one(cls, collection: str, data: dict, excluded: dict):
        obj = await cls.client[collection].insert_one(data)
        response = await cls.client[collection].find_one(
            {"_id": obj.inserted_id}, excluded
        )
        return response

    @staticmethod
    async def find_one(cls, collection: str, query: dict, excluded: dict):
        response = await cls.client[collection].find_one(query, excluded)
        return response

    @staticmethod
    async def find(
        cls, collection: str, query: dict, excluded: dict, limit: int
    ) -> List:
        response = await cls.client[collection].find(query, excluded).to_list(limit)
        return response

    @staticmethod
    async def update_one(cls, collection: str, query: dict, data: dict) -> int:
        response = await cls.client[collection].update_one(query, {"$set": data})
        return response.modified_count

    @staticmethod
    async def delete_one(cls, collection: str, query: dict) -> int:
        response = await cls.client[collection].delete_one(query)
        return response.deleted_count

    @staticmethod
    async def delete_many(cls, collection: str, query: dict) -> int:
        response = await cls.client[collection].delete_many(query)
        return response.deleted_count

    @staticmethod
    async def count(cls, collection: str, query: dict) -> int:
        response = await cls.client[collection].count_documents(query)
        return response


class MongoRepository(BaseRepository):

    excluded = {"_id": 0}
    limit = 100

    # Commons
    @classmethod
    async def list_models(cls, **kwargs) -> list:
        models = await cls.find(cls.main_model, kwargs, cls.excluded, cls.limit)
        return models

    @classmethod
    async def create_model(cls, data: dict):
        obj = await cls.create_one(cls.main_model, data, cls.excluded)
        return from_dict(Model, obj) if obj else None

    @classmethod
    async def exist_path_or_model(
        cls, path: str, model_name: str
    ) -> Union[Model, None]:
        query = {"$or": [{"path": path}, {"model": model_name}]}
        obj = await cls.find_one(cls.main_model, query, cls.excluded)
        return from_dict(Model, obj) if obj else None

    @classmethod
    async def model_by_path(cls, path: str) -> Union[Model, None]:
        obj = await cls.find_one(cls.main_model, {"path": path}, cls.excluded)
        return from_dict(Model, obj) if obj else None

    @classmethod
    async def delete_model(cls, model_name: str) -> int:
        response = await cls.delete_one(cls.main_model, {"name": model_name})
        if response.deleted_count > 0:
            await cls.client.drop_collection(model_name)
        return response.deleted_count

    @classmethod
    async def find_one_or_many(
        cls, model_name: str, resource_id: str
    ) -> Union[dict, list]:

        query = {"name": model_name}
        if resource_id:
            query = {cls.main_field: resource_id, **query}
            response = await cls.find_one(model_name, query, cls.excluded)
            return response

        rows = await cls.find(model_name, query, cls.excluded)
        return rows

    @classmethod
    async def create_row(cls, model_name: str, data: dict):
        response = await cls.create_one(model_name, data, cls.excluded)
        return response

    @classmethod
    async def update_row(cls, model_name: str, resource_id: str, data: dict) -> int:
        query = {cls.main_field: resource_id}
        updated = await cls.update_one(model_name, query, data)
        return updated

    @classmethod
    async def delete_row(cls, model_name: str, resource_id: str):
        query = {cls.main_field: resource_id}
        deleted = await cls.delete_one(model_name, query)
        return deleted
