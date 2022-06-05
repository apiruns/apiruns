from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.configs import app_configs
from api.dependencies import global_middleware
from api.exceptions import BaseException
from api.routers import get_routers


app = FastAPI(dependencies=[Depends(global_middleware)])
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_configs.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = get_routers()
for r in routers:
    app.include_router(r)


@app.exception_handler(BaseException)
async def unicorn_exception_handler(request: Request, exc: BaseException):
    """Exception handler.

    Args:
        request (Request): request object.
        exc (BaseException): Custom exception.

    Returns:
        response: exception serialized like json.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.content,
    )
