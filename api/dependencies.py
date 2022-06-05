from fastapi import Request
import json


from api.datastructures import RequestContext
from api.features.internals import features
from api.features.internals import InternalFeature
from api.exceptions import BaseException


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


async def global_middleware(request: Request):
    context = await get_context(request)
    micro = features.get(InternalFeature.MICRO)
    if micro.is_on():
        response = await micro.handle(context)
        if response.content:
            context.extras = response.content
        if response.errors:
            raise BaseException(
                content=response.errors,
                status_code=response.status_code,
            )

    request.state.input_context = context
