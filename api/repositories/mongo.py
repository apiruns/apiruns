from typing import List
from typing import Union

from dacite import from_dict

from api.configs import app_configs
from api.datastructures import Model
from api.engines import db


ADMIN_MODEL = app_configs.MODEL_ADMIN_NAME
ID_FIELD = app_configs.IDENTIFIER_ID


class MongoRepository:
    """It is the collection of queries to the mongo client."""

    @staticmethod
    async def create_one(data, model) -> dict:
        """Create a document in mongo.

        Args:
            data (dict): Data to save.
            model (str): Collection name.

        Returns:
            dict: Document created.
        """
        obj = await db[model].insert_one(data)
        response = await db[model].find_one({"_id": obj.inserted_id}, {"_id": 0})
        return response

    @staticmethod
    async def find(model, limit=app_configs.QUERY_LIMIT, params={}) -> dict:
        """Find documents in mongo.

        Args:
            model (str): Collection name.
            limit (int): Limit documents.
            params (dict): Filters.

        Returns:
            list: Documents found.
        """
        response = await db[model].find(params, {"_id": 0}).to_list(limit)
        return response

    @staticmethod
    async def count(model, params={}) -> int:
        """Quantity of documents in mongo.

        Args:
            model (str): Collection name.
            params (dict): Filters.

        Returns:
            int: number of documents found.
        """
        response = await db[model].count_documents(params)
        return response

    @staticmethod
    async def find_one(model, params={}) -> dict:
        """Get one document in mongo.

        Args:
            model (str): Collection name.
            params (dict): Filters.

        Returns:
            dict: Documents found.
        """
        response = await db[model].find_one(params, {"_id": 0})
        return response

    @staticmethod
    async def update_one(model: str, _id: str, data: dict) -> int:
        """Update one document in mongo.

        Args:
            model (str): Collection name.
            _id (str): Reference id.
            params (dict): Filters.

        Returns:
            int: Document modified count.
        """
        response = await db[model].update_one({ID_FIELD: _id}, {"$set": data})
        return response.modified_count

    @staticmethod
    async def delete_one(model, _id) -> int:
        """Delete one document in mongo.

        Args:
            model (str): Collection name.
            _id (str): Reference id.

        Returns:
            int: Document deleted count.
        """
        response = await db[model].delete_one({ID_FIELD: _id})
        return response.deleted_count

    @staticmethod
    async def exist_model(name: str) -> bool:
        """Validate existence of a model in admin model.

        Args:
            name (str): model name.

        Returns:
            bool: exist model.
        """
        rows = await db[ADMIN_MODEL].count_documents({"model": name})
        return rows > 0

    @staticmethod
    async def exist_path_or_model(path: str, model: str) -> Union[None, Model]:
        """Validate existence of the path or model in admin model.

        Args:
            path (str): path url.

        Returns:
            bool: exist path.
        """
        response = await db[ADMIN_MODEL].find_one(
            {"$or": [{"path": path}, {"model": model}]}, {"_id": 0}
        )
        if response:
            return from_dict(data_class=Model, data=response)
        return response

    @staticmethod
    async def create_admin_model(body: dict) -> dict:
        """Create a admin model.

        Args:
            body (dict): body of admin model.

        Returns:
            dict: model admin.
        """
        obj = await db[ADMIN_MODEL].insert_one(body)
        row = await db[ADMIN_MODEL].find_one({"_id": obj.inserted_id}, {"_id": 0})
        return row

    @staticmethod
    async def delete_admin_model(model: dict) -> int:
        """Delete a admin model.

        Args:
            body (dict): body of admin model.

        Returns:
            dict: model admin.
        """
        response = await db[ADMIN_MODEL].delete_one({"name": model})
        return response.deleted_count

    @staticmethod
    async def list_admin_model(username: str = None) -> List[dict]:
        """List admin models.

        Args:
            username (str, optional): Model owner. Defaults to None.

        Returns:
            List[dict]: List admin models.
        """
        query = {"username": username} if username else {}
        rows = (
            await db[ADMIN_MODEL]
            .find({"is_deleted": None, **query}, {"_id": 0})
            .to_list(100)
        )
        return rows

    @staticmethod
    async def model_by_path(path: str) -> Union[None, Model]:
        """Look for admin model by path url.

        Args:
            path (str): path url.

        Returns:
            dict: admin model
        """
        response = await db[ADMIN_MODEL].find_one({"path": path}, {"_id": 0})
        if response:
            return from_dict(data_class=Model, data=response)
        return response

    @staticmethod
    async def find_one_or_many(model, _id) -> Union[dict, List[dict]]:
        """Get one or many documents.

        Args:
            model (str): Collection name.
            _id (str): reference id.

        Returns:
            Union[dict,List[dict]]: Documents found.
        """
        if _id:
            response = await db[model].find_one({ID_FIELD: _id}, {"_id": 0})
            return response

        response = await MongoRepository.find(model)
        return response
