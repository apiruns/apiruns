import json
from typing import Tuple

from fastapi import Request

from api.datastructures import RequestContext
from api.datastructures import ResponseContext
from api.features.internals import features
from api.features.internals import InternalFeature


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
    return RequestContext(
        body=body,
        headers=request.headers,
        method=request.method,
        original_path=request.url.path,
    )


async def get_internal_feature(
    context: RequestContext,
) -> Tuple[RequestContext, ResponseContext]:
    """Get internal feature.

    Args:
        context (RequestContext): input context.

    Returns:
        ResponseContext: response context.
    """
    auth = features.get(InternalFeature.AUTHX)
    if auth.is_on():
        response = await auth.handle(context)
        if response.content:
            context.extras = response.content
        return context, response
    return context, ResponseContext()
