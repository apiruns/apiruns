from typing import Union

from api.datastructures import InputContext
from api.datastructures import ResponseContext
from api.features.internals.authx import AuthX


class InternalFeature:
    """Internal feature names"""

    AUTHX = "AUTHX"


features = {InternalFeature.AUTHX: AuthX()}


async def internal_handle(context: InputContext) -> Union[ResponseContext, None]:

    ctx_response = None
    for feature in features.values():
        if not feature.is_on:
            continue
        resp = await feature.handle(context)
        if resp.errors:
            ctx_response = resp
            break

        if resp.content:
            ctx_response = resp
            break

    return ctx_response
