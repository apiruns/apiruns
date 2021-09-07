from typing import List

from fastapi import FastAPI, status, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from api import models
from api.constants import RouterPath
from api.validators import validate
from api.repositories import repository

app = FastAPI()


@app.get("/ping")
def ping() -> models.Ping:
    """Ping api."""
    return models.Ping(pong="OK")


# Nodes admin
@app.post(RouterPath.NODES, response_model=models.Node)
async def create_node(node: models.Node):
    """Create a node."""
    payload = jsonable_encoder(node)
    await validate.node(node.model_name, node.path)
    response = await repository.create_one(payload, "nodes")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)


@app.get(RouterPath.NODES, response_model=List[models.Node])
async def list_nodes():
    """List nodes."""
    nodes = await repository.find("nodes")
    return nodes


# Node level one.
@app.get(RouterPath.LEVEL_ONE)
async def dynamic_node_level_one_get(level_one: str) -> List:
    """Get node level one"""
    node = await repository.find_one("nodes", {"path": f"/{level_one}"})
    if node is not None:
        nodes = await repository.find(node["model"])
        return nodes

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource {level_one} not found"
    )


@app.post(RouterPath.LEVEL_ONE)
async def dynamic_node_level_one_post(
    level_one: str, payload: dict = Body(...)
) -> dict:
    """Post node level one"""
    node = await repository.find_one("nodes", {"path": f"/{level_one}"})
    if node is not None:
        payload = jsonable_encoder(payload)
        errors = validate.payload(node["schema"], payload)
        if errors:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=errors)
        else:
            response = await repository.create_one(payload, node["model"])
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource {level_one} not found"
    )
