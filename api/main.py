from fastapi import FastAPI
from fastapi import Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.configs import app_configs
from api.exceptions import BaseException
from api.routers import admin, core
from api.dependencies import global_middleware
from api.features.internals import feature_handle_routes


app = FastAPI(dependencies=[Depends(global_middleware)])
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_configs.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

feature_routers = feature_handle_routes()
for r in feature_routers:
    app.include_router(r)
app.include_router(admin.router)
app.include_router(core.router)


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
