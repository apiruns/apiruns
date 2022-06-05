from .admin import router as admin_router
from .core import router as core_router
from api.configs import app_configs
from api.features.internals import feature_handle_routes


def get_routers() -> list:
    """Get all routers available.

    Returns:
        list: List of routers.
    """
    routers = []
    feature_routers = feature_handle_routes()
    if feature_routers:
        routers = feature_routers

    routers.append(core_router)
    if app_configs.ADMIN_CONTROLLER:
        routers.append(admin_router)

    return routers
