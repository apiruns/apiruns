import importlib
from typing import Any
from typing import List
from typing import Union

from api.configs import app_configs
from api.datastructures import RequestContext


class InternalFeature:
    """Internal Feature"""

    _instance = None

    def __new__(cls):
        if InternalFeature._instance is None:
            if app_configs.FEATURE_INTERNAL_PATH:
                module = importlib.import_module(app_configs.FEATURE_INTERNAL_PATH)
                InternalFeature._instance = module.main()
            else:
                InternalFeature._instance = False
        return InternalFeature._instance

    def routers(self):
        pass

    def middleware(self, context):
        pass

    def repository(self):
        pass


def get_feature_routers() -> List:
    """Routers feature.

    Returns:
        List: List of routers.
    """
    internal_feature = InternalFeature()
    if internal_feature:
        return internal_feature.routers()
    return []


async def get_feature_middleware(context) -> Union[None, RequestContext]:
    """Get feature middleware.

    Args:
        context (RequestContext): request context.

    Returns:
        Union[None, RequestContext]: Context or None.
    """
    internal_feature = InternalFeature()
    if internal_feature:
        return await internal_feature.middleware(context)
    return None


def get_feature_repository() -> Any:
    """Get feature repository.

    Returns:
        Any: Return feature repository.
    """
    internal_feature = InternalFeature()
    if internal_feature:
        return internal_feature.repository()
    return None
