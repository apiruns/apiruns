import json

from fastapi import Request

from api.datastructures import InputContext
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


async def get_context(request: Request) -> InputContext:
    """Get context from request.

    Args:
        request (Request): Request object.

    Returns:
        InputContext: Input context.
    """
    body = await validate_body(request)
    return InputContext(
        body=body,
        headers=request.headers,
        method=request.method,
        original_path=request.url.path,
        model={},
    )


async def get_internal_feature(context: InputContext) -> ResponseContext:
    """Get internal feature.

    Args:
        context (InputContext): input context.

    Returns:
        ResponseContext: response context.
    """
    auth = features.get(InternalFeature.AUTHX)
    if auth.is_on():
        return ResponseContext()
    return await auth.handle(context)
