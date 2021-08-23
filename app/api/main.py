from typing import Optional, List

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.api import models
from app.api.constants import routes
from app.api.engines import db

app = FastAPI()


@app.get("/ping")
def ping() -> models.Ping:
    return models.Ping(pong="OK")

# Nodes admin
@app.post("/admin/nodes", response_model=models.Node)
async def create_node(node: models.Node):
    student = jsonable_encoder(node)
    obj = await db["nodes"].insert_one(student)
    created_node = await db["nodes"].find_one({"_id": obj.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_node)

@app.get("/admin/nodes", response_model=List[models.Node])
async def get_nodes():
    nodes = await db["nodes"].find({}).to_list(10)
    return nodes

# Node level one.
@app.get(routes.LevelOne.PATH)
def node_level_one_get(level_one: str) -> str:
    return "one"

@app.post(routes.LevelOne.PATH)
def node_level_one_post(level_one: str) -> str:
    return "two"


# Node level two.
@app.get(routes.LevelTwo.PATH)
def node_level_two_get(level_one: str, level_two: str) -> str:
    return "one"

@app.post(routes.LevelTwo.PATH)
def node_level_two_post(level_one: str, level_two: str) -> str:
    return "two"