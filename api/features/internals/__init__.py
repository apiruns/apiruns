from typing import Union

from api.datastructures import RequestContext
from api.datastructures import ResponseContext
from api.features.internals.micro import Micro


class InternalFeature:
    """Internal feature names"""

    MICRO = "MICRO"


features = {InternalFeature.MICRO: Micro()}


async def internal_handle(context: RequestContext) -> Union[ResponseContext, None]:

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
