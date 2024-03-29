import json

from fastapi import Request

from api.datastructures import RequestContext
from api.features.config import get_feature_middleware
from api.serializers.context import ContextSerializer


async def validate_body(request: Request) -> dict:
    """Validate request body

    Args:
        request (Request): request object.

    Returns:
        dict: Json valid.
    """
    try:
        return await request.json()
    except json.decoder.JSONDecodeError:
        return {}


async def get_context(request: Request) -> RequestContext:
    """Get context from request.

    Args:
        request (Request): Request object.

    Returns:
        RequestContext: Input context.
    """
    body = await validate_body(request)
    params = ContextSerializer.query_params(request.query_params)
    return RequestContext(
        body=body,
        headers=request.headers,
        method=request.method,
        original_path=request.url.path,
        query_params=params,
    )


async def global_middleware(request: Request) -> None:
    """Global middleware.

    Args:
        request (Request): request object.
    """
    context = await get_context(request)
    context_modified = await get_feature_middleware(context)
    if context_modified:
        context = context_modified

    request.state.input_context = context
