from typing import List

from app.api import models
from fastapi import Body
from fastapi import FastAPI
from fastapi import Request

from api.configs import route_config
from api.services import service_node

app = FastAPI()


@app.get("/ping")
def ping() -> models.Ping:
    """Ping api."""
    return models.Ping(pong="OK")


# Admin model create
@app.post(route_config.RouterAdmin.ADMIN, response_model=models.Node)
async def create_model(body: models.Node):
    """Create a model."""
    response = await service_node.create_node(body)
    return response


# Admin model list
@app.get(route_config.RouterAdmin.ADMIN, response_model=List[models.Node])
async def list_models():
    """List models."""
    response = await service_node.list_nodes()
    return response


# Path level one.
@app.get(route_config.RouterPath.LEVEL_ONE)
@app.post(route_config.RouterPath.LEVEL_ONE)
async def dynamic_path_level_one(
    level_one: str,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic path level one."""
    response = await service_node.from_method(request.method, body, level_one)
    return response


# Path level two.
@app.get(route_config.RouterPath.LEVEL_TWO)
@app.put(route_config.RouterPath.LEVEL_TWO)
@app.post(route_config.RouterPath.LEVEL_TWO)
@app.patch(route_config.RouterPath.LEVEL_TWO)
@app.delete(route_config.RouterPath.LEVEL_TWO)
async def dynamic_path_level_two(
    level_one,
    level_two,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic path level two."""
    response = await service_node.from_method(
        request.method, body, level_one, level_two
    )
    return response


# Path level three.
@app.get(route_config.RouterPath.LEVEL_THREE)
@app.put(route_config.RouterPath.LEVEL_THREE)
@app.post(route_config.RouterPath.LEVEL_THREE)
@app.patch(route_config.RouterPath.LEVEL_THREE)
@app.delete(route_config.RouterPath.LEVEL_THREE)
async def dynamic_path_level_three(
    level_one,
    level_two,
    level_three,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic path level three."""
    response = await service_node.from_method(
        request.method,
        body,
        level_one,
        level_two,
        level_three,
    )
    return response


# Path level four.
@app.get(route_config.RouterPath.LEVEL_FOUR)
@app.put(route_config.RouterPath.LEVEL_FOUR)
@app.post(route_config.RouterPath.LEVEL_FOUR)
@app.patch(route_config.RouterPath.LEVEL_FOUR)
@app.delete(route_config.RouterPath.LEVEL_FOUR)
async def dynamic_path_level_four(
    level_one,
    level_two,
    level_three,
    level_four,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic path level four."""
    response = await service_node.from_method(
        request.method,
        body,
        level_one,
        level_two,
        level_three,
        level_four,
    )
    return response


# Path level five.
@app.get(route_config.RouterPath.LEVEL_FIVE)
@app.put(route_config.RouterPath.LEVEL_FIVE)
@app.post(route_config.RouterPath.LEVEL_FIVE)
@app.patch(route_config.RouterPath.LEVEL_FIVE)
@app.delete(route_config.RouterPath.LEVEL_FIVE)
async def dynamic_path_level_five(
    level_one,
    level_two,
    level_three,
    level_four,
    level_five,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic path level five."""
    response = await service_node.from_method(
        request.method,
        body,
        level_one,
        level_two,
        level_three,
        level_four,
        level_five,
    )
    return response


# Path level six.
@app.get(route_config.RouterPath.LEVEL_SIX)
@app.put(route_config.RouterPath.LEVEL_SIX)
@app.post(route_config.RouterPath.LEVEL_SIX)
@app.patch(route_config.RouterPath.LEVEL_SIX)
@app.delete(route_config.RouterPath.LEVEL_SIX)
async def dynamic_path_level_six(
    level_one,
    level_two,
    level_three,
    level_four,
    level_five,
    level_six,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic path level six."""
    response = await service_node.from_method(
        request.method,
        body,
        level_one,
        level_two,
        level_three,
        level_four,
        level_five,
        level_six,
    )
    return response


# Path level seven.
@app.get(route_config.RouterPath.LEVEL_SEVEN)
@app.put(route_config.RouterPath.LEVEL_SEVEN)
@app.patch(route_config.RouterPath.LEVEL_SEVEN)
@app.delete(route_config.RouterPath.LEVEL_SEVEN)
async def dynamic_path_level_seven(
    level_one,
    level_two,
    level_three,
    level_four,
    level_five,
    level_six,
    level_seven,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic path level seven."""
    response = await service_node.from_method(
        request.method,
        body,
        level_one,
        level_two,
        level_three,
        level_four,
        level_five,
        level_six,
        level_seven,
    )
    return response
