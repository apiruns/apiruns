from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.configs import route_config
from fastapi import Request
from fastapi import Body
from api.controllers.core import CoreController


router = APIRouter()


# Path root.
@router.get(route_config.Router.LEVEL_ROOT)
@router.post(route_config.Router.LEVEL_ROOT)
async def dynamic_path_level_root(
    request: Request,
    body: dict = Body(default={}),
):
    """Dynamic path level one."""
    msg = "full documentation https://apiruns.github.io/apiruns/"
    return JSONResponse({"docs": msg})


# Path level one.
@router.get(route_config.Router.LEVEL_ONE)
@router.post(route_config.Router.LEVEL_ONE)
@router.put(route_config.Router.LEVEL_ONE)
@router.patch(route_config.Router.LEVEL_ONE)
@router.delete(route_config.Router.LEVEL_ONE)
async def dynamic_path_level_one(request: Request, level_one: str):
    """Dynamic path level one."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level two.
@router.get(route_config.Router.LEVEL_TWO)
@router.put(route_config.Router.LEVEL_TWO)
@router.post(route_config.Router.LEVEL_TWO)
@router.patch(route_config.Router.LEVEL_TWO)
@router.delete(route_config.Router.LEVEL_TWO)
async def dynamic_path_level_two(
    request: Request,
):
    """Dynamic path level two."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level three.
@router.get(route_config.Router.LEVEL_THREE)
@router.put(route_config.Router.LEVEL_THREE)
@router.post(route_config.Router.LEVEL_THREE)
@router.patch(route_config.Router.LEVEL_THREE)
@router.delete(route_config.Router.LEVEL_THREE)
async def dynamic_path_level_three(
    request: Request,
):
    """Dynamic path level three."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level four.
@router.get(route_config.Router.LEVEL_FOUR)
@router.put(route_config.Router.LEVEL_FOUR)
@router.post(route_config.Router.LEVEL_FOUR)
@router.patch(route_config.Router.LEVEL_FOUR)
@router.delete(route_config.Router.LEVEL_FOUR)
async def dynamic_path_level_four(
    request: Request,
):
    """Dynamic path level four."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level five.
@router.get(route_config.Router.LEVEL_FIVE)
@router.put(route_config.Router.LEVEL_FIVE)
@router.post(route_config.Router.LEVEL_FIVE)
@router.patch(route_config.Router.LEVEL_FIVE)
@router.delete(route_config.Router.LEVEL_FIVE)
async def dynamic_path_level_five(
    request: Request,
):
    """Dynamic path level five."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level six.
@router.get(route_config.Router.LEVEL_SIX)
@router.put(route_config.Router.LEVEL_SIX)
@router.post(route_config.Router.LEVEL_SIX)
@router.patch(route_config.Router.LEVEL_SIX)
@router.delete(route_config.Router.LEVEL_SIX)
async def dynamic_path_level_six(
    request: Request,
):
    """Dynamic path level six."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level seven.
@router.get(route_config.Router.LEVEL_SEVEN)
@router.put(route_config.Router.LEVEL_SEVEN)
@router.patch(route_config.Router.LEVEL_SEVEN)
@router.delete(route_config.Router.LEVEL_SEVEN)
async def dynamic_path_level_seven(
    request: Request,
):
    """Dynamic path level seven."""
    response = await CoreController.handle(request.state.input_context)
    return response
