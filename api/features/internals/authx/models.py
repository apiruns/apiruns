import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import Union

import bcrypt
from dacite import from_dict

from api.configs import app_configs
from api.datastructures import BaseModel
from api.repositories import repository


@dataclass(frozen=True)
class AuthXConfig:
    """AuthX object config"""

    ON: bool
    JWT_SECRET: str
    JWT_EXP: int
    JWT_ALGORITHM: str
    MODEL: str
    SIGN_IN_PATH: str
    REGISTER_PATH: str
    ALLOWED_MODELS: int


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


class Queries:
    """Queries repositories"""

    @staticmethod
    async def find_user(model: str, username: str) -> Union[User, None]:
        """Find a user.

        Args:
            model (str): model name.
            username (str): username.

        Returns:
            Union[User, None]: User object or none.
        """
        obj = await repository.find_one(model, {"username": username})
        return from_dict(User, obj) if obj else None

    @staticmethod
    async def create_user(data: dict, model: str) -> Union[User, None]:
        """Create a user.

        Args:
            data (dict): user payload.
            model (str): mdoel name.

        Returns:
            Union[User, None]: User obj or None.
        """
        obj = await repository.create_one(data, model)
        return from_dict(User, obj) if obj else None

    @staticmethod
    async def max_models(username: str) -> int:
        """Max model by user

        Args:
            username (str): username.

        Returns:
            int: Quantity of models.
        """
        models = await repository.count(
            app_configs.MODEL_ADMIN_NAME, {"username": username}
        )
        return models
