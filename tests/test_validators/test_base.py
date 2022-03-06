import pytest
from fastapi import HTTPException

from api.validators.base import ValidatorMixin
from tests.conftest import AsyncMock


@pytest.mark.asyncio
async def test_validator_mixin_in_model_method_with_model_already_exists(mocker):
    mock_repo = mocker.patch(
        "api.repositories.repository.count", new_callable=AsyncMock
    )

    mock_repo.side_effect = [1, 0]
    v = ValidatorMixin()

    with pytest.raises(HTTPException):
        await v.model("users", "/users")


@pytest.mark.asyncio
async def test_validator_mixin_in_model_method_with_path_already_exists(mocker):
    mock_repo = mocker.patch(
        "api.repositories.repository.count", new_callable=AsyncMock
    )

    mock_repo.side_effect = [1, 1]
    v = ValidatorMixin()

    with pytest.raises(HTTPException):
        await v.model("users", "/users")


@pytest.mark.asyncio
async def test_validator_mixin_in_model_method_with_validation_ok(mocker):
    mock_repo = mocker.patch(
        "api.repositories.repository.count", new_callable=AsyncMock
    )

    mock_repo.side_effect = [0, 0]
    v = ValidatorMixin()

    expect = await v.model("users", "/users")
    assert expect is None
