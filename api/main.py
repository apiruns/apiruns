from typing import List

from fastapi import Body
from fastapi import FastAPI
from fastapi import Request

from api import models
from api.constants import RouterPath
from api.services import service_node

app = FastAPI()


@app.get("/ping")
def ping() -> models.Ping:
    """Ping api."""
    return models.Ping(pong="OK")


# Nodes admin
@app.post(RouterPath.NODES, response_model=models.Node)
async def create_node(body: models.Node):
    """Create a node."""
    response = await service_node.create_node(body)
    return response


@app.get(RouterPath.NODES, response_model=List[models.Node])
async def list_nodes():
    """List nodes."""
    response = await service_node.list_nodes()
    return response


# Node level one.
@app.get(RouterPath.LEVEL_ONE)
@app.post(RouterPath.LEVEL_ONE)
async def dynamic_node_level_one(
    level_one: str,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic node level one."""
    response = await service_node.from_method(request.method, body, level_one)
    return response


# Node level two.
@app.get(RouterPath.LEVEL_TWO)
@app.put(RouterPath.LEVEL_TWO)
@app.post(RouterPath.LEVEL_TWO)
@app.patch(RouterPath.LEVEL_TWO)
@app.delete(RouterPath.LEVEL_TWO)
async def dynamic_node_level_two(
    level_one,
    level_two,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic node level two."""
    response = await service_node.from_method(
        request.method, body, level_one, level_two
    )
    return response


# Node level three.
@app.get(RouterPath.LEVEL_THREE)
@app.put(RouterPath.LEVEL_THREE)
@app.post(RouterPath.LEVEL_THREE)
@app.patch(RouterPath.LEVEL_THREE)
@app.delete(RouterPath.LEVEL_THREE)
async def dynamic_node_level_three(
    level_one,
    level_two,
    level_three,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic node level three."""
    response = await service_node.from_method(
        request.method,
        body,
        level_one,
        level_two,
        level_three,
    )
    return response


# Node level four.
@app.get(RouterPath.LEVEL_FOUR)
@app.put(RouterPath.LEVEL_FOUR)
@app.post(RouterPath.LEVEL_FOUR)
@app.patch(RouterPath.LEVEL_FOUR)
@app.delete(RouterPath.LEVEL_FOUR)
async def dynamic_node_level_four(
    level_one,
    level_two,
    level_three,
    level_four,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic node level four."""
    response = await service_node.from_method(
        request.method,
        body,
        level_one,
        level_two,
        level_three,
        level_four,
    )
    return response


# Node level five.
@app.get(RouterPath.LEVEL_FIVE)
@app.put(RouterPath.LEVEL_FIVE)
@app.post(RouterPath.LEVEL_FIVE)
@app.patch(RouterPath.LEVEL_FIVE)
@app.delete(RouterPath.LEVEL_FIVE)
async def dynamic_node_level_five(
    level_one,
    level_two,
    level_three,
    level_four,
    level_five,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic node level five."""
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


# Node level six.
@app.get(RouterPath.LEVEL_SIX)
@app.put(RouterPath.LEVEL_SIX)
@app.post(RouterPath.LEVEL_SIX)
@app.patch(RouterPath.LEVEL_SIX)
@app.delete(RouterPath.LEVEL_SIX)
async def dynamic_node_level_six(
    level_one,
    level_two,
    level_three,
    level_four,
    level_five,
    level_six,
    request: Request,
    body: dict = Body(...),
):
    """Dynamic node level six."""
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


# Node level seven.
@app.get(RouterPath.LEVEL_SEVEN)
@app.put(RouterPath.LEVEL_SEVEN)
@app.patch(RouterPath.LEVEL_SEVEN)
@app.delete(RouterPath.LEVEL_SEVEN)
async def dynamic_node_level_seven(
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
    """Dynamic node level seven."""
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
