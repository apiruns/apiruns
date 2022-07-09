from typing import List
from typing import Union

from dacite import from_dict

from api.configs import app_configs
from api.datastructures import Model
from api.engines import db


class BaseRepository:
    """Base repository"""

    main_model = app_configs.MODEL_ADMIN_NAME
    main_field = app_configs.IDENTIFIER_ID
    client = db
    query_limit = app_configs.MONGO_PAGINATION_LIMIT
    query_skip = 0

    @classmethod
    async def create_one(
        cls, collection: str, data: dict, excluded: dict
    ) -> Union[dict, None]:
        """Create an object.

        Args:
            collection (str): Collection name.
            data (dict): Data to save.
            excluded (dict): Query to exclude.

        Returns:
            Union[dict, None]: Return `dict` if object was created else `None`
        """
        obj = await cls.client[collection].insert_one(data)
        response = await cls.client[collection].find_one(
            {"_id": obj.inserted_id}, excluded
        )
        return response

    @classmethod
    async def find_one(
        cls, collection: str, query: dict, excluded: dict
    ) -> Union[dict, None]:
        """Get an object.

        Args:
            collection (str): Collection name.
            query (dict): search.
            excluded (dict): Query to exclude.

        Returns:
            Union[dict, None]: Return `dict` if object was found else `None`
        """
        response = await cls.client[collection].find_one(query, excluded)
        return response

    @classmethod
    async def find(
        cls, collection: str, query: dict, excluded: dict, skip: int, limit: int
    ) -> List:
        """List objects.

        Args:
            collection (str): Collection name.
            query (dict): search.
            excluded (dict): Query to exclude.
            skip: skip search.
            limit: limit search.

        Returns:
            list: Return list of object found.
        """
        response = (
            await cls.client[collection]
            .find(query, excluded)
            .skip(skip)
            .limit(limit)
            .to_list(limit)
        )
        return response

    @classmethod
    async def update_one(cls, collection: str, query: dict, data: dict) -> int:
        """Update an object.

        Args:
            collection (str): Collection name.
            query (dict): search.
            data (dict): Data to update.

        Returns:
            int: Return object updated.
        """
        response = await cls.client[collection].update_one(query, {"$set": data})
        return response.modified_count

    @classmethod
    async def update_many(cls, collection: str, query: dict, data: dict) -> int:
        """Update many objects.

        Args:
            collection (str): Collection name.
            query (dict): search.
            data (dict): Data to update.

        Returns:
            int: Return object updated.
        """
        response = await cls.client[collection].update_many(query, {"$set": data})
        return response.modified_count

    @classmethod
    async def delete_one(cls, collection: str, query: dict) -> int:
        """Delete an object.

        Args:
            collection (str): Collection name.
            query (dict): search.

        Returns:
            int: Return object deleted.
        """
        response = await cls.client[collection].delete_one(query)
        return response.deleted_count

    @classmethod
    async def delete_many(cls, collection: str, query: dict) -> int:
        """Delete many objects.

        Args:
            collection (str): Collection name.
            query (dict): search.

        Returns:
            int: Return objects deleted.
        """
        response = await cls.client[collection].delete_many(query)
        return response.deleted_count

    @classmethod
    async def count(cls, collection: str, query: dict) -> int:
        """Get when objects are found.

        Args:
            collection (str): Collection name.
            query (dict): search.

        Returns:
            int: objects found.
        """
        response = await cls.client[collection].count_documents(query)
        return response


class MongoRepository(BaseRepository):
    """Mongo repository"""

    excluded = {"_id": 0}  # Fields excluded

    @classmethod
    def get_pagination(cls, params: dict):
        limit = params.get("limit")
        page = params.get("page")
        limit = cls.query_limit if not limit else limit
        page = cls.query_skip if not page else page
        skip = (limit * page) if page else page
        return skip, limit

    # Commons
    @classmethod
    async def list_models(cls, **kwargs) -> list:
        """List models.

        Returns:
            list: Models found.
        """
        models = await cls.find(
            cls.main_model, kwargs, cls.excluded, 0, cls.query_limit
        )
        return models

    @classmethod
    async def create_model(cls, data: dict) -> Union[Model, None]:
        """Create a model.

        Args:
            data (dict): Data required by model object.

        Returns:
            Union[Model, None]: Return `Model` if was success else `None`.
        """
        obj = await cls.create_one(cls.main_model, data, cls.excluded)
        return from_dict(Model, obj) if obj else None

    @classmethod
    async def exist_path_or_model(
        cls, path: str, model_name: str
    ) -> Union[Model, None]:
        """Find model exists from path or name.

        Args:
            path (str): request path.
            model_name (str): model name.

        Returns:
            Union[Model, None]: Return `Model` if was success else `None`.
        """
        query = {"$or": [{"path": path}, {"model": model_name}]}
        obj = await cls.find_one(cls.main_model, query, cls.excluded)
        return from_dict(Model, obj) if obj else None

    @classmethod
    async def model_by_path(cls, path: str) -> Union[Model, None]:
        """Find model from path.

        Args:
            path (str): Path request.

        Returns:
            Union[Model, None]: Return `Model` if was success else `None`.
        """
        obj = await cls.find_one(cls.main_model, {"path": path}, cls.excluded)
        return from_dict(Model, obj) if obj else None

    @classmethod
    async def delete_model(cls, model_name: str) -> int:
        """Delete model.

        Args:
            model_name (str): Model name.

        Returns:
            int: Return model deleted.
        """
        deleted_count = await cls.delete_one(cls.main_model, {"name": model_name})
        if deleted_count > 0:
            await cls.client.drop_collection(model_name)
        return deleted_count

    @classmethod
    async def find_one_or_many(
        cls,
        model_name: str,
        resource_id: str,
        query_params: dict,
    ) -> Union[dict, list, None]:
        """Find one or more rows.

        Args:
            model_name (str): Model name.
            resource_id (str): Resource id.
            query_params (dict): query params.

        Returns:
            Union[dict, list, None]: Return `None` if was not found else list or dict.
        """
        if resource_id:
            query = {cls.main_field: resource_id}
            response = await cls.find_one(model_name, query, cls.excluded)
            return response

        skip, limit = cls.get_pagination(query_params)
        rows = await cls.find(model_name, {}, cls.excluded, skip, limit)
        return rows

    @classmethod
    async def create_row(cls, model_name: str, data: dict) -> Union[dict, None]:
        """Create a row.

        Args:
            model_name (str): Model name.
            data (dict): Data required.

        Returns:
            Union[dict, None]: Return data created.
        """
        response = await cls.create_one(model_name, data, cls.excluded)
        return response

    @classmethod
    async def update_row(cls, model_name: str, resource_id: str, data: dict) -> int:
        """Update a row.

        Args:
            model_name (str): Model name.
            resource_id (str): Resource id.
            data (dict): Data to update.

        Returns:
            int: Row deleted.
        """
        query = {cls.main_field: resource_id}
        updated = await cls.update_one(model_name, query, data)
        return updated

    @classmethod
    async def delete_row(cls, model_name: str, resource_id: str):
        """Delete a row.

        Args:
            model_name (str): Model name.
            resource_id (str): Resource id.

        Returns:
            int: Row deleted.
        """
        query = {cls.main_field: resource_id}
        deleted = await cls.delete_one(model_name, query)
        return deleted
