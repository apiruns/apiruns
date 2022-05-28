from fastapi import status
from fastapi.responses import JSONResponse

from api.datastructures import RequestContext
from api.features.internals import features
from api.features.internals import InternalFeature


class MicroController:
    """Micro feature interal controller"""

    @classmethod
    async def create_user(cls, context: RequestContext) -> JSONResponse:
        """Create a user.

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        micro = features.get(InternalFeature.MICRO)
        if not micro.is_on():
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": f"Resource `{context.original_path}` not found !"},
            )
        response = await micro.create_user(context.body)
        return response.json_response()

    @classmethod
    async def users_sign(cls, context: RequestContext) -> JSONResponse:
        """User sign.

        Args:
            context (RequestContext): request context.

        Returns:
            JSONResponse: response.
        """
        micro = features.get(InternalFeature.MICRO)
        if not micro.is_on():
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": f"Resource `{context.original_path}` not found !"},
            )
        response = await micro.authentication(context.body)
        return response.json_response()

    @classmethod
    async def user(cls, context: RequestContext, username: str) -> JSONResponse:
        """Get username.

        Args:
            context (RequestContext): Request context.
            username (str): username.

        Returns:
            JSONResponse: response OK if exist user else NOT_FOUND.
        """
        micro = features.get(InternalFeature.MICRO)
        if not micro.is_on():
            return JSONResponse(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                content={"error": "Method Not Allowed"},
            )
        response = await micro.exist_user(username)
        return response.json_response()
