from fastapi import status
from fastapi.responses import JSONResponse

from api.configs import route_config as rt
from api.datastructures import RequestContext
from api.repositories import repository
from api.serializers.admin import AdminSerializer


class AdminController:
    """Admin Controller"""

    @classmethod
    async def create_model(cls, context: RequestContext) -> JSONResponse:
        """Create a model.

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        valid, data = AdminSerializer.validate_admin_model(context.body)
        if not valid:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=data,
            )
        if data.path in rt.RouterAdmin.excluded():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "the path already exists, is admin path."},
            )

        # TODO: Move to internal feature handle.
        if "username" in context.extras:
            data.username = context.extras.get("username")
            data.name = f"{data.username}_{data.name}"
            data.path = f"/{data.username}{data.path}"

        model = await repository.exist_path_or_model(data.path, data.name)
        if model:
            name = "path" if model.path == data.path else "model"
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": f"the {name} already exists."},
            )

        response = await repository.create_admin_model(data.to_json())
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

    @classmethod
    async def list_models(cls, context: RequestContext) -> list:
        """List models.

        Returns:
            list: List of models.
        """
        username = None
        if "username" in context.extras:
            username = context.extras.get("username")

        return await repository.list_admin_model(username)

    @classmethod
    async def delete_model(cls, context: RequestContext) -> JSONResponse:
        """Delete a model.

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        valid, errors = AdminSerializer.validate_delete(context.body)
        if not valid:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=errors)

        await repository.delete_admin_model(context.body)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
