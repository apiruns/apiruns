from api.engines import db


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
    async def find(model, limit, params) -> dict:
        """Find documents in mongo.

        Args:
            model (str): Collection name.
            limit (int): Limit documents.
            params (dict): Filters.

        Returns:
            list: Documents found.
        """
        response = (
            await db[model]
            .find({"is_active": True, **params}, {"_id": 0})
            .to_list(limit)
        )
        return response

    @staticmethod
    async def count(model, params) -> int:
        """Quantity of documents in mongo.

        Args:
            model (str): Collection name.
            params (dict): Filters.

        Returns:
            int: number of documents found.
        """
        response = await db[model].count_documents({"is_active": True, **params})
        return response

    @staticmethod
    async def find_one(model, params) -> dict:
        """Get one document in mongo.

        Args:
            model (str): Collection name.
            params (dict): Filters.

        Returns:
            dict: Documents found.
        """
        response = await db[model].find_one({"is_active": True, **params})
        return response
