import os
from typing import Tuple


class RouterAdmin:
    """Router admin contants"""

    ADMIN = os.environ.get("MAIN_ADMIN_PATH", "/admin/models")
    # Internal feature
    AUTHX_SIGN_IN = "/admin/users/signin"
    AUTHX_REGISTER = "/admin/users"

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
            cls.AUTHX_SIGN_IN,
            cls.AUTHX_REGISTER,
            cls.PING,
        )

    @classmethod
    def is_excluded(cls, path_list: list) -> bool:
        """Validate if a path exist in the excluded.

        Args:
            path_list (list): path list.

        Returns:
            bool: _description_
        """
        exist = False
        for p in path_list:
            exist = p in cls.excluded()
            if exist:
                break
        return exist


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
