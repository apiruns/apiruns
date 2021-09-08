import uuid
from api.utils.node import build_path_from_params, paths_with_slash
from fastapi import status, HTTPException, Body
from fastapi.responses import JSONResponse
from api.repositories import repository
from fastapi.encoders import jsonable_encoder
from api.validators import validate


class ServiceNodeMongo:
    """Service Node for mongo."""

    @staticmethod
    async def create_node(body: Body):
        """Create an node document in mongo"""
        await validate.node(body.model_name, body.path)
        payload = jsonable_encoder(body)
        response = await repository.create_one(payload, "nodes")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

    @staticmethod
    async def list_nodes():
        """List node documents in mongo"""
        nodes = await repository.find(model="nodes", params={"is_active": True})
        return nodes

    @staticmethod
    async def get(*args):
        """Is the method get for dynamic node"""
        original_path, modified_path, _id = build_path_from_params(args)
        nodes = await repository.find(
            model="nodes", params={"path": {"$in": paths_with_slash(modified_path)}}
        )
        if nodes:
            node = nodes[0]
            if _id:
                response = await repository.find_one(
                    node["model"], {"reference_id": _id}
                )
            else:
                response = await repository.find(node["model"])
            return response

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{original_path}` not found !",
        )

    @staticmethod
    async def post(body, *args):
        """Is the method post for dynamic node"""
        original_path, modified_path, _ = build_path_from_params(args)
        nodes = await repository.find(
            model="nodes", params={"path": {"$in": paths_with_slash(modified_path)}}
        )
        if nodes:
            node = nodes[0]
            payload = jsonable_encoder(body)
            errors = validate.payload(node["schema"], payload)
            if errors:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST, content=errors
                )
            else:
                payload["reference_id"] = str(uuid.uuid4())
                document = await repository.create_one(payload, node["model"])
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED, content=document
                )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{original_path}` not found !",
        )
