from typing import List
from fastapi import HTTPException


def custom_http_exception(
    status_code: int, loc: List[str], msg: str, type_name: str, errors: dict
) -> HTTPException:
    """Http exception from params.

    Args:
        status_code (int): Status code.
        loc (List[str]): List loc.
        msg (str): Error menssage.
        type_name (str): Error type.
        errors (dict): Error json.

    Returns:
        HTTPException: Exception of fastapi.
    """
    return HTTPException(
        status_code, [{"loc": loc, "msg": msg, "type": type_name, "errors": errors}]
    )
