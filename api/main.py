from fastapi import Body
from fastapi import FastAPI
from fastapi import Request

from api.configs import route_config
from api.services import service_model
from fastapi import HTTPException
from fastapi import status

app = FastAPI()


@app.get("/ping")
def ping() -> dict:
    """Ping api."""
    return {"pong": "OK"}


# Admin model create
@app.post(route_config.RouterAdmin.ADMIN)
async def create_model(request: Request): 
    """Create a model.""" 
    try: 
        response = await service_model.create_model(await request.json())
        return response
    except: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Body requeried",
        )

# Admin model list
@app.get(route_config.RouterAdmin.ADMIN)
async def list_models():
    """List models."""
    response = await service_model.list_models()
    return response

# Admin model delete
@app.delete(route_config.RouterAdmin.ADMIN)
async def list_models(request: Request):
    """List models."""
    try: 
        response = await service_model.delete_model(await request.json())
        return response
    except: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Body requeried",
        )

# Path root.
@app.get(route_config.Router.LEVEL_ROOT)
@app.post(route_config.Router.LEVEL_ROOT)
async def dynamic_path_level_root(
    request: Request,
    body: dict = Body(default={}),
):
    """Dynamic path level one."""
    response = await service_model.get_service_method(request.method, body)
    return response


# Path level one.
@app.get(route_config.Router.LEVEL_ONE)
@app.post(route_config.Router.LEVEL_ONE)
async def dynamic_path_level_one(
    level_one: str,
    request: Request,
    body: dict = Body(default={}),
):
    """Dynamic path level one."""
    response = await service_model.get_service_method(request.method, body, level_one)
    return response


# Path level two.
@app.get(route_config.Router.LEVEL_TWO)
@app.put(route_config.Router.LEVEL_TWO)
@app.post(route_config.Router.LEVEL_TWO)
@app.patch(route_config.Router.LEVEL_TWO)
@app.delete(route_config.Router.LEVEL_TWO)
async def dynamic_path_level_two(
    level_one,
    level_two,
    request: Request,
    body: dict = Body(default={}),
):
    """Dynamic path level two."""
    response = await service_model.get_service_method(
        request.method, body, level_one, level_two
    )
    return response


# Path level three.
@app.get(route_config.Router.LEVEL_THREE)
@app.put(route_config.Router.LEVEL_THREE)
@app.post(route_config.Router.LEVEL_THREE)
@app.patch(route_config.Router.LEVEL_THREE)
@app.delete(route_config.Router.LEVEL_THREE)
async def dynamic_path_level_three(
    level_one,
    level_two,
    level_three,
    request: Request,
    body: dict = Body(default={}),
):
    """Dynamic path level three."""
    response = await service_model.get_service_method(
        request.method,
        body,
        level_one,
        level_two,
        level_three,
    )
    return response


# Path level four.
@app.get(route_config.Router.LEVEL_FOUR)
@app.put(route_config.Router.LEVEL_FOUR)
@app.post(route_config.Router.LEVEL_FOUR)
@app.patch(route_config.Router.LEVEL_FOUR)
@app.delete(route_config.Router.LEVEL_FOUR)
async def dynamic_path_level_four(
    level_one,
    level_two,
    level_three,
    level_four,
    request: Request,
    body: dict = Body(default={}),
):
    """Dynamic path level four."""
    response = await service_model.get_service_method(
        request.method,
        body,
        level_one,
        level_two,
        level_three,
        level_four,
    )
    return response


# Path level five.
@app.get(route_config.Router.LEVEL_FIVE)
@app.put(route_config.Router.LEVEL_FIVE)
@app.post(route_config.Router.LEVEL_FIVE)
@app.patch(route_config.Router.LEVEL_FIVE)
@app.delete(route_config.Router.LEVEL_FIVE)
async def dynamic_path_level_five(
    level_one,
    level_two,
    level_three,
    level_four,
    level_five,
    request: Request,
    body: dict = Body(default={}),
):
    """Dynamic path level five."""
    response = await service_model.get_service_method(
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
@app.get(route_config.Router.LEVEL_SIX)
@app.put(route_config.Router.LEVEL_SIX)
@app.post(route_config.Router.LEVEL_SIX)
@app.patch(route_config.Router.LEVEL_SIX)
@app.delete(route_config.Router.LEVEL_SIX)
async def dynamic_path_level_six(
    level_one,
    level_two,
    level_three,
    level_four,
    level_five,
    level_six,
    request: Request,
    body: dict = Body(default={}),
):
    """Dynamic path level six."""
    response = await service_model.get_service_method(
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
@app.get(route_config.Router.LEVEL_SEVEN)
@app.put(route_config.Router.LEVEL_SEVEN)
@app.patch(route_config.Router.LEVEL_SEVEN)
@app.delete(route_config.Router.LEVEL_SEVEN)
async def dynamic_path_level_seven(
    level_one,
    level_two,
    level_three,
    level_four,
    level_five,
    level_six,
    level_seven,
    request: Request,
    body: dict = Body(default={}),
):
    """Dynamic path level seven."""
    response = await service_model.get_service_method(
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
