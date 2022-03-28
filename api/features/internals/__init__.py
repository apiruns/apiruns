from typing import Union

from api.datastructures import InputContext
from api.datastructures import ResponseContext
from api.features.internals import AuthX

features = {"AUTHX": AuthX()}


def internal_handle(context: InputContext) -> Union[ResponseContext, None]:

    ctx_response = None
    for feature in features:
        if not feature.is_on:
            continue
        resp = feature.handle(context)
        if resp.errors:
            ctx_response = resp
            break

        if resp.context:
            context.body = resp.context

    return ctx_response
