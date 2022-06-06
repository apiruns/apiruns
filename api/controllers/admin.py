from fastapi import status
from fastapi.responses import JSONResponse

from api.configs import route_config as rt
from api.datastructures import RequestContext
from api.repositories import repository_from_feature
from api.serializers.admin import AdminSerializer


class AdminController:
    """Admin Controller"""

    repository = repository_from_feature()

    @classmethod
    async def handle(cls, context: RequestContext) -> JSONResponse:
        """Handle from methods.

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        allowed = {
            rt.HTTPMethod.POST: cls.create_model,
            rt.HTTPMethod.GET: cls.list_models,
            rt.HTTPMethod.DELETE: cls.delete_model,
        }
        fn = allowed.get(context.method)
        if not fn:
            return JSONResponse(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                content={"error": "Method Not Allowed"},
            )
        return await fn(context)

    @classmethod
    async def create_model(cls, context: RequestContext) -> JSONResponse:
        """Create a model.

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        valid, model_p = AdminSerializer.validate_admin_model(context.body)
        if not valid:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=model_p,
            )
        if model_p.path in rt.RouterAdmin.excluded():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "the path already exists, is admin path."},
            )

        model = await cls.repository.exist_path_or_model(model_p.path, model_p.name)
        if model:
            name = "path" if model.path == model_p.path else "model"
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": f"the {name} already exists."},
            )

        response = await cls.repository.create_model(model_p.to_json())
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content=response.to_json()
        )

    @classmethod
    async def list_models(cls, context: RequestContext) -> list:
        """List models.

        Returns:
            list: List of models.
        """
        models = await cls.repository.list_models()
        return JSONResponse(content=models)

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

        await cls.repository.delete_model(context.body.get("name"))
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
