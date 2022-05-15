from fastapi import Response
from fastapi import status
from fastapi.responses import JSONResponse

from api.configs import route_config as rt
from api.datastructures import RequestContext
from api.repositories import repository
from api.serializers.core import CoreSerializer


class CoreController:
    """Core Controller"""

    @classmethod
    async def handle(cls, context: RequestContext) -> JSONResponse:
        """Define the service to use according to the http method."""
        repositories = {
            rt.HTTPMethod.POST: cls.post,
            rt.HTTPMethod.GET: cls.get,
            rt.HTTPMethod.PUT: cls.put,
            rt.HTTPMethod.PATCH: cls.put,
            rt.HTTPMethod.DELETE: cls.delete,
        }
        service = repositories.get(context.method)
        if not service:
            return JSONResponse(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                content={"error": "Method Not Allowed"},
            )

        return await service(context)

    @classmethod
    async def get(cls, context: RequestContext) -> JSONResponse:
        """Get method

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        model = await repository.model_by_path(context.path)
        if model:
            response = await repository.find_one_or_many(
                model.name, context.resource_id
            )
            if response is not None:
                return response

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Resource `{context.original_path}` not found !"},
        )

    @classmethod
    async def post(cls, context: RequestContext) -> JSONResponse:
        """Post method

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        if context.resource_id:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": f"Resource `{context.original_path}` not found !"},
            )

        model = await repository.model_by_path(context.path)
        if model:
            valid, data = CoreSerializer.validate(context.body, model.schema)
            if not valid:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST, content=data
                )

            obj = await repository.create_one(data, model.name)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=obj)

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Resource `{context.original_path}` not found !"},
        )

    @classmethod
    async def put(cls, context: RequestContext) -> JSONResponse:
        """Put method

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        model = await repository.model_by_path(context.path)
        if model:
            valid, data = CoreSerializer.validate_update(context.body, model.schema)
            if not valid:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST, content=data
                )
            await repository.update_one(model.name, context.resource_id, data)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Resource `{context.original_path}` not found !"},
        )

    @classmethod
    async def delete(cls, context: RequestContext) -> JSONResponse:
        """Delete method

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        model = await repository.model_by_path(context.path)
        if model:
            await repository.delete_one(model.name, context.resource_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Resource `{context.original_path}` not found !"},
        )
