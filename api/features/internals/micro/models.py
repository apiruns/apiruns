import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import Union

import bcrypt
from dacite import from_dict

from api.configs import app_configs
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
    """Get micro feature configuration.

    Returns:
        MicroConfig: Object config by micro feature.
    """
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
        """Set properties"""
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
    """Micro repository"""

    excluded = {"_id": 0}  # Params excluded in queries.
    limit = 50  # Query limit configuration.
    _config = get_config()  # Get micro feature configuration.

    # Users
    @classmethod
    async def find_user(cls, username: str) -> Union[User, None]:
        """Find a user in micro feature.

        Args:
            username (str): username in micro feature.

        Returns:
            Union[User, None]: Return `User` if was success else `None`.
        """
        obj = await cls.find_one(
            cls._config.USER_MODEL, {"username": username}, cls.excluded
        )
        return from_dict(User, obj) if obj else None

    @classmethod
    async def create_user(cls, data: dict) -> Union[User, None]:
        """Create an user in micro feature.

        Args:
            data (dict): Data required by user model.

        Returns:
            Union[User, None]: Return `User` if was success else `None`.
        """
        obj = await cls.create_one(cls._config.USER_MODEL, data, cls.excluded)
        return from_dict(User, obj) if obj else None

    @classmethod
    async def max_models_by_user(cls, username: str) -> int:
        """Maximum models allowed by a user.

        Args:
            username (str): username.

        Returns:
            int: Maximum models allowed.
        """
        models = await cls.count(cls._config.MODEL, {"username": username})
        return models

    # Commons
    @classmethod
    async def list_models(cls, **kwargs) -> list:
        """List models.

        Returns:
            list: Return list models.
        """
        models = await cls.find(cls._config.MODEL, kwargs, cls.excluded, cls.limit)
        return models

    @classmethod
    async def create_model(cls, data: dict) -> Union[Model, None]:
        """Create a model.

        Args:
            data (dict): Data required by model object.

        Returns:
            Union[Model, None]: Return `Model` if was success else `None`.
        """
        obj = await cls.create_one(cls._config.MODEL, data, cls.excluded)
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
        obj = await cls.find_one(cls._config.MODEL, query, cls.excluded)
        return from_dict(Model, obj) if obj else None

    @classmethod
    async def model_by_path(cls, path: str) -> Union[Model, None]:
        """Find model from path.

        Args:
            path (str): Path request.

        Returns:
            Union[Model, None]: Return `Model` if was success else `None`.
        """
        obj = await cls.find_one(cls._config.MODEL, {"path": path}, cls.excluded)
        return from_dict(Model, obj) if obj else None

    @classmethod
    async def delete_model(cls, model_name: str) -> int:
        """Delete model.

        Args:
            model_name (str): Model name.

        Returns:
            int: Return model deleted.
        """
        query = {"name": model_name}
        deleted = await cls.delete_one(cls._config.MODEL, query)
        if deleted > 0:
            await cls.delete_many(cls._config.MODEL_ROWS, query)
        return deleted

    @classmethod
    async def find_one_or_many(
        cls, model_name: str, resource_id: str
    ) -> Union[dict, list, None]:
        """Find one or more rows.

        Args:
            model_name (str): Model name.
            resource_id (str): Resource id.

        Returns:
            Union[dict, list, None]: Return `None` if was not found else list or dict.
        """
        query = {"name": model_name}
        if resource_id:
            query = {cls.main_field: resource_id, **query}
            response = await cls.find_one(cls._config.MODEL_ROWS, query, cls.excluded)
            return response.get("data") if response else None

        rows = await cls.find(cls._config.MODEL_ROWS, query, cls.excluded, cls.limit)
        return [row.get("data") for row in rows]

    @classmethod
    async def create_row(cls, model_name: str, data: dict) -> Union[dict, None]:
        """Create a row.

        Args:
            model_name (str): Model name.
            data (dict): Data required.

        Returns:
            Union[dict, None]: Return data created.
        """
        data = {
            "name": model_name,
            cls.main_field: data.get(cls.main_field),
            "data": data,
        }
        obj = await cls.create_one(cls._config.MODEL_ROWS, data, cls.excluded)
        return obj.get("data") if obj else None

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
        query = {cls.main_field: resource_id, "name": model_name}
        data = {**query, "data": data}
        updated = await cls.update_one(cls._config.MODEL_ROWS, query, data)
        return updated

    @classmethod
    async def delete_row(cls, model_name: str, resource_id: str) -> int:
        """Delete a row.

        Args:
            model_name (str): Model name.
            resource_id (str): Resource id.

        Returns:
            int: Row deleted.
        """
        query = {cls.main_field: resource_id, "name": model_name}
        deleted = await cls.delete_one(cls._config.MODEL_ROWS, query)
        return deleted
