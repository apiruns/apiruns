from typing import Optional, List

from fastapi import FastAPI, status, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.api import models
from app.api.constants import routes
from app.api.engines import db
from app.api.meta import get_meta_validator

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
async def list_nodes():
    nodes = await db["nodes"].find({}).to_list(10)
    return nodes

# Node level one.
@app.get(routes.LevelOne.PATH)
async def node_level_one_get(level_one: str) -> List:
    obj = await db["nodes"].find_one({"path": f"/{level_one}", "is_active": True})
    if obj is not None:
        nodes = await db[obj["algo"]].find({}, {"_id": 0}).to_list(10)
        return nodes

    raise HTTPException(status_code=404, detail=f"Resource {level_one} not found")

@app.post(routes.LevelOne.PATH)
async def node_level_one_post(level_one: str, payload: dict = Body(...)) -> dict:
    obj = await db["nodes"].find_one({"path": f"/{level_one}", "is_active": True})
    if obj is not None:
        validator = get_meta_validator(obj["structure"])
        try:
            este = validator(**payload)
            response = await db[obj["algo"]].insert_one(jsonable_encoder(payload))
            return payload
        except ValidationError as e:
            print(e.json())

    raise HTTPException(status_code=400, detail=f"Resource {level_one} not found")


# Node level two.
@app.get(routes.LevelTwo.PATH)
def node_level_two_get(level_one: str, level_two: str) -> str:
    return "one"

@app.post(routes.LevelTwo.PATH)
def node_level_two_post(level_one: str, level_two: str) -> str:
    return "two"