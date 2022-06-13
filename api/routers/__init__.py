from .admin import router as admin_router
from .core import router as core_router
from api.features.config import get_feature_routes


def get_routers() -> list:
    """Get all routers available.

    Returns:
        list: List of routers.
    """
    routers = []
    feature_routers = get_feature_routes()
    if feature_routers:
        routers = feature_routers
        routers.append(core_router)
        return routers

    routers.append(admin_router)
    routers.append(core_router)
    return routers
