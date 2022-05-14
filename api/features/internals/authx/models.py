from dataclasses import dataclass
from dataclasses import field
from typing import Union

import bcrypt
from dacite import from_dict

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


@dataclass
class User(BaseModel):
    """User Model.

    Args:
        BaseModel: Base model.
    """

    password: str = ""
    email: str = ""
    username: str = ""
    verified: bool = field(default_factory=lambda: False)

    def protected(self) -> None:
        """protect password field."""
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
    async def find_user(model: str, email: str) -> Union[User, None]:
        """Find a user.

        Args:
            model (str): model name.
            email (str): user email.

        Returns:
            Union[User, None]: User object or none.
        """
        obj = await repository.find_one(model, {"username": email})
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
