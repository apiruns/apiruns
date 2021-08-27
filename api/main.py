from typing import Optional, List

from fastapi import FastAPI, status, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from api import models
from api.constants.routes import Paths
from api.engines import db
from api.validators import validate
from api.repositories import repository

app = FastAPI()


@app.get("/ping")
def ping() -> models.Ping:
    return models.Ping(pong="OK")

# Nodes admin
@app.post("/admin/nodes", response_model=models.Node)
async def create_node(node: models.Node):
    payload = jsonable_encoder(node)
    response = await repository.create_one(payload, "nodes")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

@app.get("/admin/nodes", response_model=List[models.Node])
async def list_nodes():
    nodes = await repository.find("nodes")
    return nodes

# Node level one.
@app.get(Paths.LEVEL_ONE)
async def node_level_one_get(level_one: str) -> List:
    node = await repository.find_one("nodes", {"path": f"/{level_one}"})
    if node is not None:
        nodes = await repository.find(node["model"])
        return nodes

    raise HTTPException(status_code=404, detail=f"Resource {level_one} not found")

@app.post(Paths.LEVEL_ONE)
async def node_level_one_post(level_one: str, payload: dict = Body(...)) -> dict:
    node = await repository.find_one("nodes", {"path": f"/{level_one}"})
    if node is not None:
        payload = jsonable_encoder(payload)
        errors = validate.payload(node["schema"], payload)
        if errors:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=errors)
        else:
            response = await repository.create_one(payload, node["model"])
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

    raise HTTPException(status_code=404, detail=f"Resource {level_one} not found")
