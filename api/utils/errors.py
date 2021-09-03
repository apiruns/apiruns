import json
from typing import List
from fastapi import HTTPException


def custom_http_exception(status_code: int, loc: List[str], msg: str, type_name: str, errors: dict) -> HTTPException:
    return HTTPException(
        status_code,
        [{
            "loc": loc,
            "msg": msg,
            "type": type_name,
            "errors": errors
        }]
    )
