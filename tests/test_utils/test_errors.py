import pytest
from fastapi import HTTPException

from api.utils.errors import custom_http_exception


def test_call_http_exception_with_params():
    exception = custom_http_exception(
        200, ["body", "model"], "This is a msg.", "validation", {}
    )
    assert isinstance(exception, HTTPException)
    with pytest.raises(HTTPException):
        raise exception
