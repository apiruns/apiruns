import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import Union
from api.configs import app_configs

import bcrypt
from dacite import from_dict

from api.datastructures import BaseModel
from api.datastructures import Model
from api.repositories import Base


@dataclass(frozen=True)
class MicroConfig:
    """Micro object config"""

    ON: bool
    JWT_SECRET: str
    JWT_EXP: int
    JWT_ALGORITHM: str
    MODEL: str
    SIGN_IN_PATH: str
    REGISTER_PATH: str
    ALLOWED_MODELS: int
    USER_MODEL: str
    MODEL_ROWS: str


def get_config() -> MicroConfig:
    configs = app_configs.INTERNALS.get("MICRO")
    return from_dict(MicroConfig, configs)


@dataclass
class User(BaseModel):
    """User Model.

    Args:
        BaseModel: Base model.
    """

    password: str = ""
    email: str = ""
    username: str = ""
    allowed_models: int = 0
    verified: bool = field(default_factory=lambda: False)

    def __post_init__(self):
        self.public_id = str(uuid.uuid4())

    def protected(self) -> None:
        """Protect password field."""
        p = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt(10))
        self.password = p.decode()

    def check(self, password: str) -> bool:
        """Validate password encode.

        Args:
            password (str): password encode

        Returns:
            bool: True is password valid.
        """
        p = password.encode("utf-8")
        return bcrypt.checkpw(p, self.password.encode("utf-8"))

    def to_response(self) -> dict:
        """Return user obj like json.

        Returns:
            dict: user like json.
        """
        r = self.to_json()
        del r["password"]
        return r


class Repository(Base):
    """Micro repositories"""

    excluded = {"_id": 0}
    limit = 50
    _config = get_config()

    # Users
    @classmethod
    async def find_user(cls, username: str) -> Union[User, None]:
        obj = await cls.find_one(
            cls._config.USER_MODEL, {"username": username}, cls.excluded
        )
        return from_dict(User, obj) if obj else None

    @classmethod
    async def create_user(cls, data: dict) -> Union[User, None]:
        obj = await cls.create_one(cls._config.USER_MODEL, data)
        return from_dict(User, obj) if obj else None

    @classmethod
    async def max_models_by_user(cls, username: str) -> int:
        models = await cls.count(cls._config.MODEL, {"username": username})
        return models

    # Commons
    @classmethod
    async def list_models(cls, **kwargs):
        models = await cls.find(cls._config.MODEL_ROWS, kwargs, cls.excluded, cls.limit)
        return models

    @classmethod
    async def create_model(cls, data: dict):
        obj = await cls.create_one(cls._config.MODEL, data, cls.excluded)
        return from_dict(Model, obj) if obj else None

    @classmethod
    async def exist_path_or_model(cls, path: str, model_name: str):
        query = {"$or": [{"path": path}, {"model": model_name}]}
        obj = await cls.find_one(cls._config.MODEL, query, cls.excluded)
        return from_dict(Model, obj) if obj else None

    @classmethod
    async def model_by_path(cls, path: str) -> int:
        obj = await cls.find_one(cls._config.MODEL, {"path": path}, cls.excluded)
        return from_dict(Model, obj) if obj else None

    @classmethod
    async def delete_model(cls, model_name: str) -> int:
        query = {"name": model_name}
        deleted = await cls.delete_many(cls._config.MODEL_ROWS, query)
        return deleted

    @classmethod
    async def find_one_or_many(
        cls, model_name: str, resource_id: str
    ) -> Union[dict, list]:

        query = {"name": model_name}
        if resource_id:
            query = {cls.main_field: resource_id, **query}
            response = await cls.find_one(cls._config.MODEL_ROWS, query, cls.excluded)
            return response

        rows = await cls.find(cls._config.MODEL_ROWS, query, cls.excluded)
        return rows

    @classmethod
    async def create_row(cls, model_name: str, data: dict):
        data = {
            "name": model_name,
            cls.main_field: data.get(cls.main_field),
            "data": data,
        }
        obj = await cls.create_one(cls._config.MODEL_ROWS, data, cls.excluded)
        return obj

    @classmethod
    async def update_row(cls, model_name: str, resource_id: str, data: dict) -> int:
        query = {cls.main_field: resource_id, "name": model_name}
        data = {**query, "data": data}
        updated = await cls.update_one(cls._config.MODEL_ROWS, query, data)
        return updated

    @classmethod
    async def delete_row(cls, model_name: str, resource_id: str):
        query = {cls.main_field: resource_id, "name": model_name}
        deleted = await cls.delete_one(cls._config.MODEL_ROWS, query)
        return deleted
