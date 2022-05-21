from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt
from dacite import from_dict
from fastapi import status

from .models import AuthXConfig
from .models import Queries
from .models import User
from .serializers import AuthXSerializer
from api.configs import app_configs
from api.configs import route_config
from api.datastructures import RequestContext
from api.datastructures import ResponseContext


class AuthX:
    """AuthX internal feature"""

    # errors
    HEADER_REQUIRED = {"error": "`Authorization` header is required"}
    HEADER_SCHEMA_REQUIRED = {"error": "Token schema is required as `Bearer <token>`"}
    TOKEN_EXPIRED = {"error": "Your token has expired"}
    TOKEN_INVALID = {"error": "Your token is invalid"}
    EMAIL_EXIST = {"error": "email already exists"}
    USER_EXIST = {"error": "username already exists"}
    USER_NOT_CREATED = {"error": "user not created"}
    AUTH_FAILED = {"error": "username or password wrong"}
    FORBIDDEN = {"error": "you do not have permission to consume this resource."}

    def __init__(self):
        configs = app_configs.INTERNALS.get("AUTHX")
        self.configs = from_dict(AuthXConfig, configs)

    async def handle(self, context: RequestContext) -> ResponseContext:
        """Handle feature entrypoint.

        Args:
            context (RequestContext): Input context.

        Returns:
            response (ResponseContext): response context.
        """
        if self.is_path_excluded(context.path):
            return ResponseContext()

        response = self.decode(context.headers)
        if response.content:
            return self._has_permission(response, context.path)
        return response

    def _has_permission(self, response: ResponseContext, path: str) -> ResponseContext:
        """Current user has permission.
        Args:
            response (ResponseContext): response.
            path (str): current path.

        Returns:
            ResponseContext: response.
        """
        if route_config.RouterAdmin.ADMIN == path:
            return response

        current_user = response.content.get("username")
        path_split = path.split("/")
        root = path_split[1] if len(path_split) > 1 else current_user
        if current_user != root:
            return ResponseContext(
                errors=self.FORBIDDEN, status_code=status.HTTP_403_FORBIDDEN
            )

        return response

    def is_path_excluded(self, path) -> bool:
        """Validate if is a path excluded.

        Args:
            path (str): request path.

        Returns:
            bool: True if is excluded.
        """
        excluded = (
            route_config.RouterAdmin.PING,
            route_config.RouterAdmin.AUTHX_USER,
            route_config.RouterAdmin.AUTHX_SIGN_IN,
        )
        return path in excluded

    def is_on(self) -> bool:
        """Feature is On or Off.

        Returns:
            bool: return true is ON or false is OFF.
        """
        return self.configs.ON

    def encode(self, **kwargs: dict) -> str:
        """Create JWT token.

        Args:
            kwargs: Extra args for payload.

        Returns:
            str: Token encode.
        """
        exp = datetime.now(tz=timezone.utc) + timedelta(seconds=self.configs.JWT_EXP)
        default = {"exp": exp, "iat": datetime.now(tz=timezone.utc)}
        token = jwt.encode(
            {**kwargs, **default},
            self.configs.JWT_SECRET,
            algorithm=self.configs.JWT_ALGORITHM,
        )
        return token

    def decode(self, headers: dict) -> ResponseContext:
        """Decode JWT token.

        Args:
            headers (dict): request headers.

        Raises:
            ValueError: Header invalid.

        Returns:
            ResponseContext: response context.
        """
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
            payload = jwt.decode(
                t_value, self.configs.JWT_SECRET, algorithms=self.configs.JWT_ALGORITHM
            )
            return ResponseContext(content=payload)
        except jwt.ExpiredSignatureError:
            return ResponseContext(
                errors=self.TOKEN_EXPIRED, status_code=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.InvalidTokenError:
            return ResponseContext(
                errors=self.TOKEN_INVALID, status_code=status.HTTP_401_UNAUTHORIZED
            )

    async def authentication(self, payload: dict) -> ResponseContext:
        """Authenticate user.

        Args:
            payload (dict): payload request.
            example:
                {
                    "username": "user",
                    "password": "secret"
                }

        Returns:
            ResponseContext: response context.
        """
        errors = AuthXSerializer.validate_login(payload)
        if errors:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=errors
            )

        user = await Queries.find_user(self.configs.MODEL, payload.get("username"))
        if not user:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=self.AUTH_FAILED
            )

        valid = user.check(payload.get("password"))
        if not valid:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=self.AUTH_FAILED
            )

        token = self.encode(username=user.username)
        return ResponseContext(
            status_code=status.HTTP_200_OK,
            content={"token": token, **user.to_response()},
        )

    async def create_user(self, payload: dict) -> ResponseContext:
        """Create a new user.

        Args:
            payload (dict): payload request.
            example:
                {
                    "username": "user",
                    "password": "secret"
                }

        Returns:
            ResponseContext: response context.
        """
        errors = AuthXSerializer.validate_login(payload)
        if errors:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=errors
            )

        user = await Queries.find_user(self.configs.MODEL, payload.get("username"))
        if user:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=self.USER_EXIST
            )
        user_unverified = from_dict(User, payload)
        user_unverified.protected()

        user = await Queries.create_user(user_unverified.to_dict(), self.configs.MODEL)
        if not user:
            return ResponseContext(
                status_code=status.HTTP_400_BAD_REQUEST, errors=self.USER_NOT_CREATED
            )

        content = user.to_response()
        content["token"] = self.encode(username=user.username)
        return ResponseContext(status_code=status.HTTP_201_CREATED, content=content)

    async def exist_user(self, username: str) -> ResponseContext:
        """Exist username.

        Args:
            username (str): username.

        Returns:
            ResponseContext: response OK if exist user else NOT_FOUND.
        """
        user = await Queries.find_user(self.configs.MODEL, username)
        if user:
            return ResponseContext(status_code=status.HTTP_200_OK, content={})

        return ResponseContext(status_code=status.HTTP_404_NOT_FOUND, content={})
