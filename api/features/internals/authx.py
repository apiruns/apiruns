from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from typing import Union

import bcrypt
import jwt
from dacite import from_dict
from fastapi import status

from api.configs import app_configs
from api.datastructures import BaseModel
from api.datastructures import InputContext
from api.datastructures import ResponseContext
from api.repositories import repository
from api.validators import validate


@dataclass(frozen=True)
class AuthXConfig:
    ON: bool
    JWT_SECRET: str
    JWT_EXP: int
    JWT_ALGORITHM: str
    MODEL: str
    SIGN_IN_PATH: str
    REGISTER_PATH: str


@dataclass
class User(BaseModel):
    password: str = ""
    email: str = ""

    def protected(self) -> None:
        p = self.password.encode("utf-8")
        self.password = bcrypt.hashpw(p, bcrypt.gensalt(10))

    def check(self, password: str) -> bool:
        p = password.encode("utf-8")
        return bcrypt.checkpw(p, self.password)

    def to_response(self):
        r = self.to_json()
        del r["password"]
        return r


class Queries:
    @staticmethod
    async def find_user(model: str, email: str) -> Union[User, None]:
        obj = repository.find_one(model, {"email": email})
        if obj:
            return from_dict(User, obj)
        return

    @staticmethod
    async def create_user(data: dict, model: str) -> Union[User, None]:
        obj = repository.create_one(data, model)
        if obj:
            return from_dict(User, obj)
        return


class AuthX:

    # errors
    HEADER_REQUIRED = {"error": "`Authorization` header is required"}
    HEADER_SCHEMA_REQUIRED = {"error": "Token schema is required as `Bearer <token>`"}
    TOKEN_EXPIRED = {"error": "Your token has expired"}
    TOKEN_INVALID = {"error": "Your token is invalid"}
    EMAIL_EXIST = {"error": "email already exists"}
    USER_NOT_CREATED = {"error": "user not created"}
    AUTH_FAILED = {"error": "email or password wrong"}

    # validations
    CERBERUS_USER_SCHEMA = {
        "email": {
            "type": "string",
            "regex": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        },
        "password": {
            "type": "string",
            "regex": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$",  # no-qa
        },
    }

    def __init__(self):
        configs = app_configs["INTERNALS"].get("AUTHX")
        self.configs = from_dict(AuthXConfig, configs)

    async def handle(self, context: InputContext):
        if (
            self.configs.SIGN_IN_PATH == context.model["path"]
            and context.method == "POST"
        ):
            resp = await self.authentication(context.body)
            return resp

        if (
            self.configs.REGISTER_PATH == context.model["path"]
            and context.method == "POST"
        ):
            resp = await self.create_user(context.body)
            return resp

        return self.authorization(context.model, context.headers)

    def is_on(self) -> bool:
        return self.configs.ON

    def from_config(self, config: dict) -> None:
        self.configs = from_dict(AuthXConfig, config)
        return self.configs

    def encode(self, payload: dict) -> str:
        exp = datetime.timedelta(seconds=self.configs.JWT_EXP)
        default = {"exp": exp, "iat": datetime.now(tz=timezone.utc)}
        token_bytes = jwt.encode(
            {**payload, **default}, self.configs.JWT_SECRET, algorithm=self.ALGORITHM
        )
        return token_bytes.decode()

    def decode(self, headers: dict) -> ResponseContext:
        authorization_h = headers.get("Authorization")
        if not authorization_h:
            return ResponseContext(
                errors=self.HEADER_REQUIRED, status_code=status.HTTP_401_UNAUTHORIZED
            )

        try:
            if "Bearer" not in authorization_h:
                raise ValueError
            t_type, t_value = authorization_h.split(" ")
        except ValueError:
            return ResponseContext(
                errors=self.HEADER_SCHEMA_REQUIRED,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            p = jwt.decode(
                t_value, app_configs.JWT_SECRET, algorithms=self.config.ALGORITHM
            )
            return ResponseContext(
                content={"payload": p},
            )
        except jwt.ExpiredSignatureError:
            return ResponseContext(
                errors=self.TOKEN_EXPIRED, status_code=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.InvalidTokenError:
            return ResponseContext(
                errors=self.TOKEN_INVALID, status_code=status.HTTP_401_UNAUTHORIZED
            )

    def authorization(self, model: dict, headers: dict) -> ResponseContext:
        if "protected" not in model:
            return ResponseContext()
        return self.decode(headers)

    async def authentication(self, payload: dict) -> ResponseContext:
        errors = validate.data_is_valid(self.CERBERUS_USER_SCHEMA, payload)
        if errors:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=errors
            )

        user = await Queries.find_user(self.MODEL, payload.get("email"))
        if not user:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=self.AUTH_FAILED
            )

        valid = user.check(payload.get("password"))
        if not valid:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=self.AUTH_FAILED
            )

        token = self.encode({"iss": user.public_id})
        return ResponseContext(
            status_code=status.HTTP_200_OK,
            content={"token": token, **user.to_response()},
        )

    async def create_user(self, payload: dict) -> ResponseContext:
        errors = validate.data_is_valid(self.CERBERUS_USER_SCHEMA, payload)
        if errors:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=errors
            )

        user = await Queries.find_user(self.MODEL, payload.get("email"))
        if user:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=self.EMAIL_EXIST
            )
        user_unverified = from_dict(User, payload)
        user_unverified.protected()

        user = await Queries.create_user(user_unverified.to_json(), self.MODEL)
        if not user:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=self.USER_NOT_CREATED
            )

        return ResponseContext(
            status_code=status.HTTP_201_CREATED, content=user.to_response()
        )
