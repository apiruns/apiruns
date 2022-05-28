import os
from typing import Tuple


class RouterAdmin:
    """Router admin contants"""

    ADMIN = os.environ.get("MAIN_ADMIN_PATH", "/admin/models")
    # Internal feature
    MICRO_SIGN_IN = "/admin/users/signin"
    MICRO_USER = "/admin/users"

    # ping
    PING = os.environ.get("PING_ADMIN_PATH", "/ping")

    @classmethod
    def excluded(cls) -> Tuple:
        """Path excluded.

        Returns:
            Tuple: path list.
        """
        return (
            cls.ADMIN,
            cls.MICRO_SIGN_IN,
            cls.MICRO_USER,
            cls.PING,
        )


class Router:
    """Router constants"""

    LEVEL_ROOT = "/"
    LEVEL_ONE = "/{level_one}"
    LEVEL_TWO = "/{level_one}/{level_two}"
    LEVEL_THREE = "/{level_one}/{level_two}/{level_three}"
    LEVEL_FOUR = "/{level_one}/{level_two}/{level_three}/{level_four}"
    LEVEL_FIVE = "/{level_one}/{level_two}/{level_three}/{level_four}/" "{level_five}"
    LEVEL_SIX = (
        "/{level_one}/{level_two}/{level_three}/{level_four}"
        "/{level_five}/{level_six}"
    )
    LEVEL_SEVEN = (
        "/{level_one}/{level_two}/{level_three}/{level_four}"
        "/{level_five}/{level_six}/{level_seven}"
    )


class HTTPMethod:
    """Http Methods"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

    # Other
    ALL = "ALL"

    @classmethod
    def to_list(cls):
        """Return list of methods.

        Returns:
            list: list of methods.
        """
        return [
            cls.GET,
            cls.POST,
            cls.PUT,
            cls.PATCH,
            cls.DELETE,
        ]

    @classmethod
    def modifiable(cls):
        """Return modifiable method.

        Returns:
            list: list of methods.
        """
        return [
            cls.PUT,
            cls.PATCH,
            cls.DELETE,
        ]

    @classmethod
    def static(cls):
        """Return static method.

        Returns:
            list: list of methods.
        """
        return cls.to_list() + [cls.ALL]

    @classmethod
    def get_status_code(cls, method):
        """Return status code from method.

        Returns:
            list: status code default.
        """
        return {
            cls.GET: 200,
            cls.POST: 201,
            cls.PUT: 200,
            cls.PATCH: 200,
            cls.DELETE: 204,
        }.get(method)
