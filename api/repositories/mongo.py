from api.engines import db


class MongoRepository:

    @staticmethod
    async def create_one(data, model) -> dict:
        obj = await db[model].insert_one(data)
        response = await db[model].find_one({"_id": obj.inserted_id}, {"_id": 0})
        return response

    @staticmethod
    async def find(model, limit, params) -> dict:
        response = await db[model].find({"is_active": True, **params}, {"_id": 0}).to_list(limit)
        return response

    @staticmethod
    async def count(model, params) -> int:
        response = await db[model].count_documents({"is_active": True, **params})
        return response

    @staticmethod
    async def find_one(model, params) -> dict:
        response = await db[model].find_one({"is_active": True, **params})
        return response
