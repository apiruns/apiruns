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

        model = await repository.model_by_path(context.path)
        if not model:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": f"Resource `{context.original_path}` not found !"},
            )
        context.model = model

        if model.static:
            return cls.static_response(context)

        if not context.resource_id and context.method in rt.HTTPMethod.modifiable():
            return JSONResponse(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                content={"error": "Method Not Allowed"},
            )

        response = await service(context)
        return cls.custom_response(context, response)

    @classmethod
    def static_response(cls, context) -> JSONResponse:
        if rt.HTTPMethod.ALL in context.model.static:
            static_response = context.model.static_response(context.method)
            return cls.custom_response(context, static_response)

        if context.method not in context.model.static:
            return JSONResponse(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                content={"error": "Method Not Allowed"},
            )

        static_response = context.model.static_response(context.method)
        return cls.custom_response(context, static_response)

    @classmethod
    def custom_response(cls, context, response) -> JSONResponse:
        """Response custom.

        Args:
            context (RequestContext): request context.
            response (JSONResponse): json response.

        Returns:
            JSONResponse: response.
        """
        custom_status = context.model.status_code.get(context.method)
        if context.model.status_code and custom_status:
            response.status_code = custom_status
            return response

        return response

    @classmethod
    async def get(cls, context: RequestContext) -> JSONResponse:
        """Get method

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        response = await repository.find_one_or_many(
            context.model.name, context.resource_id
        )
        if response is not None:
            return JSONResponse(content=response)

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

        valid, data = CoreSerializer.validate(context.body, context.model.schema)
        if not valid:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)

        obj = await repository.create_one(data, context.model.name)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=obj)

    @classmethod
    async def put(cls, context: RequestContext) -> JSONResponse:
        """Put method

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        valid, data = CoreSerializer.validate_update(context.body, context.model.schema)
        if not valid:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)
        await repository.update_one(context.model.name, context.resource_id, data)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="")

    @classmethod
    async def delete(cls, context: RequestContext) -> JSONResponse:
        """Delete method

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        await repository.delete_one(context.model.name, context.resource_id)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="")
