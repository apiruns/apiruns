from fastapi import status
from api.repositories import repository
from api.utils.errors import custom_http_exception
from api.utils.node import paths_with_slash


class ValidatorMixin:
    """Mixin base validator"""

    @staticmethod
    async def node(model, path) -> None:
        """Validate node params."""
        result = await repository.count("nodes", {"model": model})
        if result:
            raise custom_http_exception(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                loc=["body", "model"],
                msg="the model already exists.",
                type_name="model",
                errors=None,
            )

        result = await repository.count(
            "nodes", {"path": {"$in": paths_with_slash(path)}}
        )
        if result:
            raise custom_http_exception(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                loc=["body", "model"],
                msg="the path already exists.",
                type_name="path",
                errors=None,
            )
