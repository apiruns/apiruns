import uuid

from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from api.configs import app_configs
from api.configs import route_config
from api.configs import route_config as rt
from api.datastructures import InputContext
from api.repositories import repository
from api.utils.common import get_or_create_model
from api.utils.common import paths_without_slash
from api.validators import validate


class ServiceModelMongo:
    """Service Model for mongo."""

    @staticmethod
    async def delete_model(body: dict):
        errors, body = validate.admin_delete(body=body)
        if errors:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"error": errors}
            )

        response = await repository.delete_admin_model(body)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=response)

    @staticmethod
    async def create_model(context: InputContext):
        """Create a model document in mongo"""
        errors, body = validate.admin_model(body=context.body)
        if errors:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"error": errors}
            )

        model = get_or_create_model(body.get("model"))
        path = paths_without_slash(context.body.get("path"))
        if path in route_config.RouterAdmin.excluded():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "the path already exists, is admin path."},
            )

        obj = await repository.exist_path_or_model(path, model)
        if obj:
            name = "path" if obj.get("path") == path else "model"
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": f"the {name} already exists."},
            )

        body["model"] = model
        body["path"] = path
        response = await repository.create_admin_model(body)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

    @staticmethod
    async def list_models():
        """List models documents in mongo"""
        models = await repository.list_admin_model()
        return models

    @staticmethod
    async def get_service_method(context: InputContext):
        """Define the service to use according to the http method."""
        repositories = {
            rt.HTTPMethod.POST: ServiceModelMongo.post,
            rt.HTTPMethod.GET: ServiceModelMongo.get,
            rt.HTTPMethod.PUT: ServiceModelMongo.put,
            rt.HTTPMethod.PATCH: ServiceModelMongo.put,
            rt.HTTPMethod.DELETE: ServiceModelMongo.delete,
        }
        service = repositories.get(context.method)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Method Not Allowed",
            )

        response = await service(context)
        return response

    @staticmethod
    async def get(context):
        """Get method return an object from model."""
        model = await repository.model_by_path(context.path)
        if model:
            response = await repository.find_one_or_many(
                model["model"], context.resource_id
            )
            if response is not None:
                return response

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{context.original_path}` not found !",
        )

    @staticmethod
    async def post(context):
        """Post method create a new object."""
        if context.resource_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource `{context.original_path}` not found !",
            )

        model = await repository.model_by_path(context.path)
        if model:
            payload = context.body
            errors = validate.data_is_valid(model["schema"], payload)
            if errors:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST, content=errors
                )
            else:
                payload[app_configs.IDENTIFIER_ID] = str(uuid.uuid4())
                document = await repository.create_one(payload, model["model"])
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED, content=document
                )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{context.original_path}` not found !",
        )

    @staticmethod
    async def put(context):
        """Put method can modify the object."""
        model = await repository.model_by_path(context.path)
        if model:
            payload = context.body
            errors = validate.data_is_valid(model["schema"], payload)
            if errors:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST, content=errors
                )
            else:
                await repository.update_one(
                    model["model"], context.resource_id, payload
                )
                return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{context.original_path}` not found !",
        )

    @staticmethod
    async def delete(context):
        """Delete method can delete an object."""
        model = await repository.model_by_path(context.path)
        if model:
            await repository.delete_one(model["model"], context.resource_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{context.original_path}` not found !",
        )
