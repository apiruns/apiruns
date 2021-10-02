import uuid

from fastapi import Body
from fastapi import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from api.constants import HTTPMethod
from api.repositories import repository
from api.utils.node import build_path_from_params
from api.utils.node import paths_with_slash
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
    async def from_method(method, body, *args):
        """Define the service to use according to the http method."""
        if method == HTTPMethod.POST:
            response = await ServiceNodeMongo.post(body, args)

        elif method == HTTPMethod.DELETE:
            response = await ServiceNodeMongo.delete(args)

        elif method == HTTPMethod.GET:
            response = await ServiceNodeMongo.get(args)

        elif method in [HTTPMethod.PUT, HTTPMethod.PATCH]:
            response = await ServiceNodeMongo.put(body, args)
        else:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Method Not Allowed",
            )
        return response

    @staticmethod
    async def get(args):
        """Is the method get for dynamic node"""
        original_path, modified_path, _id = build_path_from_params(args)
        nodes = await repository.find(
            model="nodes", params={"path": {"$in": paths_with_slash(modified_path)}}
        )
        if nodes:
            node = nodes[0]
            if not _id:
                response = await repository.find(node["model"])
                return response

            response = await repository.find_one(node["model"], {"reference_id": _id})
            if response:
                return response

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{original_path}` not found !",
        )

    @staticmethod
    async def post(body, args):
        """Is the method post for dynamic node"""
        original_path, modified_path, _id = build_path_from_params(args)
        if _id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource `{original_path}` not found !",
            )

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

    @staticmethod
    async def put(body, args):
        """Is the method put for dynamic node"""
        original_path, modified_path, _id = build_path_from_params(args)
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
                await repository.update_one(
                    node["model"], {"reference_id": _id}, {"$set": payload}
                )
                return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{original_path}` not found !",
        )

    @staticmethod
    async def delete(args):
        """Is the method delete for dynamic node"""
        original_path, modified_path, _id = build_path_from_params(args)
        nodes = await repository.find(
            model="nodes", params={"path": {"$in": paths_with_slash(modified_path)}}
        )
        if nodes:
            node = nodes[0]
            await repository.delete_one(node["model"], {"reference_id": _id})
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource `{original_path}` not found !",
        )
