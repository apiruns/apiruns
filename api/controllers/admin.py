from fastapi import status
from fastapi.responses import JSONResponse

from api.configs import route_config as rt
from api.datastructures import RequestContext
from api.features.internals import features
from api.features.internals import InternalFeature
from api.repositories import repository
from api.serializers.admin import AdminSerializer


class AdminController:
    """Admin Controller"""

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

        auth = features.get(InternalFeature.AUTHX)
        if auth.is_on():
            model_p = await auth.creation_model_validation(model_p, context)

        model = await repository.exist_path_or_model(model_p.path, model_p.name)
        if model:
            name = "path" if model.path == model_p.path else "model"
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": f"the {name} already exists."},
            )

        response = await repository.create_admin_model(model_p.to_json())
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

        models = await repository.list_admin_model(username)
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

        await repository.delete_admin_model(context.body.get("name"))
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
