from fastapi import Body
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from api.configs import app_configs
from api.configs import route_config
from api.controllers.admin import AdminController
from api.controllers.core import CoreController
from api.controllers.feature import AuthXController
from api.middleware import get_context
from api.middleware import get_internal_feature

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_configs.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def app_entry(request: Request, call_next):
    """Request handle middleware"""
    context = await get_context(request)
    context, resp = await get_internal_feature(context)
    if resp.errors:
        return resp.json_response()

    request.state.input_context = context
    response = await call_next(request)
    return response


# API Health
@app.get(route_config.RouterAdmin.PING)
def ping() -> dict:
    """Ping api."""
    return {"pong": "OK"}


# Admin model create
@app.post(route_config.RouterAdmin.ADMIN)
async def create_model(request: Request):
    """Create a model."""
    response = await AdminController.create_model(request.state.input_context)
    return response


# Admin model list
@app.get(route_config.RouterAdmin.ADMIN)
async def list_models():
    """List models."""
    response = await AdminController.list_models()
    return response


# Admin create users
@app.post(route_config.RouterAdmin.AUTHX_REGISTER)
async def create_users(request: Request):
    """Create users."""
    return await AuthXController.create_user(request.state.input_context)


# Admin users sign in
@app.post(route_config.RouterAdmin.AUTHX_SIGN_IN)
async def users_sign(request: Request):
    """Users sign in."""
    return await AuthXController.users_sign(request.state.input_context)


# Path root.
@app.get(route_config.Router.LEVEL_ROOT)
@app.post(route_config.Router.LEVEL_ROOT)
async def dynamic_path_level_root(
    request: Request,
    body: dict = Body(default={}),
):
    """Dynamic path level one."""
    return {}


# Path level one.
@app.get(route_config.Router.LEVEL_ONE)
@app.post(route_config.Router.LEVEL_ONE)
async def dynamic_path_level_one(request: Request, level_one: str):
    """Dynamic path level one."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level two.
@app.get(route_config.Router.LEVEL_TWO)
@app.put(route_config.Router.LEVEL_TWO)
@app.post(route_config.Router.LEVEL_TWO)
@app.patch(route_config.Router.LEVEL_TWO)
@app.delete(route_config.Router.LEVEL_TWO)
async def dynamic_path_level_two(
    request: Request,
):
    """Dynamic path level two."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level three.
@app.get(route_config.Router.LEVEL_THREE)
@app.put(route_config.Router.LEVEL_THREE)
@app.post(route_config.Router.LEVEL_THREE)
@app.patch(route_config.Router.LEVEL_THREE)
@app.delete(route_config.Router.LEVEL_THREE)
async def dynamic_path_level_three(
    request: Request,
):
    """Dynamic path level three."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level four.
@app.get(route_config.Router.LEVEL_FOUR)
@app.put(route_config.Router.LEVEL_FOUR)
@app.post(route_config.Router.LEVEL_FOUR)
@app.patch(route_config.Router.LEVEL_FOUR)
@app.delete(route_config.Router.LEVEL_FOUR)
async def dynamic_path_level_four(
    request: Request,
):
    """Dynamic path level four."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level five.
@app.get(route_config.Router.LEVEL_FIVE)
@app.put(route_config.Router.LEVEL_FIVE)
@app.post(route_config.Router.LEVEL_FIVE)
@app.patch(route_config.Router.LEVEL_FIVE)
@app.delete(route_config.Router.LEVEL_FIVE)
async def dynamic_path_level_five(
    request: Request,
):
    """Dynamic path level five."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level six.
@app.get(route_config.Router.LEVEL_SIX)
@app.put(route_config.Router.LEVEL_SIX)
@app.post(route_config.Router.LEVEL_SIX)
@app.patch(route_config.Router.LEVEL_SIX)
@app.delete(route_config.Router.LEVEL_SIX)
async def dynamic_path_level_six(
    request: Request,
):
    """Dynamic path level six."""
    response = await CoreController.handle(request.state.input_context)
    return response


# Path level seven.
@app.get(route_config.Router.LEVEL_SEVEN)
@app.put(route_config.Router.LEVEL_SEVEN)
@app.patch(route_config.Router.LEVEL_SEVEN)
@app.delete(route_config.Router.LEVEL_SEVEN)
async def dynamic_path_level_seven(
    request: Request,
):
    """Dynamic path level seven."""
    response = await CoreController.handle(request.state.input_context)
    return response
