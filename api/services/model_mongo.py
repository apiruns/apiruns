import uuid

from fastapi import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from api.configs import app_configs
from api.configs import route_config as rt
from api.repositories import repository
from api.utils.node import build_path_from_params
from api.utils.node import paths_with_slash
from api.validators import validate


class ServiceModelMongo:
    """Service Model for mongo."""

    @staticmethod
    async def create_model(body: dict):
        """Create a model document in mongo"""
        errors, body = validate.admin_model(body=body)
        if errors:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"error": errors}
            )

        model = body.get("model") if body.get("model") else str(uuid.uuid4())
        exist_model = await repository.exist_model(model)
        if exist_model:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "the model already exists."},
            )

        exist_path = await repository.exist_path(paths_with_slash(body.get("path")))
        if exist_path:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "the path already exists."},
            )
        # TODO: This validation can be one query

        response = await repository.create_admin_model(body)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

    @staticmethod
    async def list_models():
        """List models documents in mongo"""
        models = await repository.list_admin_model()
        return models

    @staticmethod
    async def get_service_method(method, body, *args):
        """Define the service to use according to the http method."""
        repositories = {
            rt.HTTPMethod.POST: ServiceModelMongo.post,
            rt.HTTPMethod.GET: ServiceModelMongo.get,
            rt.HTTPMethod.PUT: ServiceModelMongo.put,
            rt.HTTPMethod.PATCH: ServiceModelMongo.put,
            rt.HTTPMethod.DELETE: ServiceModelMongo.delete,
        }
        service = repositories.get(method)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Method Not Allowed",
            )

        response = await service(body, args)
        return response

    @staticmethod
    async def get(body, args):
        """Get method return an object from model."""
        original_path, modified_path, _id = build_path_from_params(args)
        model = await repository.model_by_path(paths_with_slash(modified_path))
        if model:
            response = await repository.find_one_or_many(model["model"], _id)
            if response is not None:
                return response

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{original_path}` not found !",
        )

    @staticmethod
    async def post(body, args):
        """Post method create a new object."""
        original_path, modified_path, _id = build_path_from_params(args)
        if _id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource `{original_path}` not found !",
            )

        model = await repository.model_by_path(paths_with_slash(modified_path))
        if model:
            payload = jsonable_encoder(body)
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
            detail=f"Resource `{original_path}` not found !",
        )

    @staticmethod
    async def put(body, args):
        """Put method can modify the object."""
        original_path, modified_path, _id = build_path_from_params(args)
        model = await repository.model_by_path(paths_with_slash(modified_path))
        if model:
            payload = jsonable_encoder(body)
            errors = validate.data_is_valid(model["schema"], payload)
            if errors:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST, content=errors
                )
            else:
                await repository.update_one(model["model"], _id, payload)
                return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{original_path}` not found !",
        )

    @staticmethod
    async def delete(body, args):
        """Delete method can delete an object."""
        original_path, modified_path, _id = build_path_from_params(args)
        model = await repository.model_by_path(paths_with_slash(modified_path))
        if model:
            await repository.delete_one(model["model"], _id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{original_path}` not found !",
        )
