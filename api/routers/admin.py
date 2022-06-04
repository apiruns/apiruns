from fastapi import Request
from fastapi import APIRouter
from api.configs import route_config
from api.controllers.admin import AdminController


router = APIRouter()


# API Health
@router.get(route_config.RouterAdmin.PING)
def ping(request: Request) -> dict:
    """Ping api."""
    return {"pong": "OK"}


# Admin models
@router.get(route_config.RouterAdmin.ADMIN)
@router.post(route_config.RouterAdmin.ADMIN)
@router.delete(route_config.RouterAdmin.ADMIN)
async def models(request: Request):
    """Models endpoints."""
    response = await AdminController.handle(request.state.input_context)
    return response
