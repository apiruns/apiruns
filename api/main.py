from typing import List

from fastapi import FastAPI, Body
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
async def dynamic_node_level_one_get(level_one: str) -> List:
    """Get node level one."""
    response = await service_node.get(level_one)
    return response


@app.post(RouterPath.LEVEL_ONE)
async def dynamic_node_level_one_post(
    level_one: str, payload: dict = Body(...)
) -> dict:
    """Post node level one."""
    response = await service_node.post(payload, level_one)
    return response


# Node level two.
@app.get(RouterPath.LEVEL_TWO)
async def dynamic_node_level_two_get(level_one, level_two) -> List:
    """Get node level two."""
    response = await service_node.get(level_one, level_two)
    return response


@app.post(RouterPath.LEVEL_TWO)
async def dynamic_node_level_two_post(
    level_one, level_two, payload: dict = Body(...)
) -> dict:
    """Post node level two."""
    response = await service_node.post(payload, level_one, level_two)
    return response
