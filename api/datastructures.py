import json
import uuid
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from datetime import timezone
from typing import Any
from typing import Union

from fastapi import status
from fastapi.responses import JSONResponse

from api.configs import route_config
from api.utils import json_serial
from api.utils import paths_without_slash
from api.utils import split_uuid_path


@dataclass
class BaseModel:
    """Field bases"""

    public_id: Union[str, None] = None
    created_at: Union[datetime, str, None] = datetime.now(timezone.utc)
    updated_at: Union[datetime, str, None] = datetime.now(timezone.utc)
    deleted_at: Union[datetime, str, None] = None

    def to_dict(self) -> dict:
        """Convert obj to dict"""
        return asdict(self)

    def to_json(self) -> dict:
        """Convert obj to json"""
        return json.loads(
            json.dumps(self.to_dict(), indent=4, sort_keys=False, default=json_serial)
        )


@dataclass
class Feature:
    """Features allowed"""

    internal: dict = field(default_factory=dict)
    externals: dict = field(default_factory=dict)


@dataclass
class Model(BaseModel):
    """Admin Model"""

    path: Union[None, str] = None
    name: Union[None, str] = None
    schema: dict = field(default_factory=dict)
    status_code: dict = field(default_factory=dict)
    static: Union[None, dict] = None
    features: Feature = field(default_factory=Feature)

    def __post_init__(self):
        if not self.public_id:
            self.public_id = str(uuid.uuid4())
        if not self.path:
            self.path = paths_without_slash(self.path.strip().lower())
        if self.name:
            self.name = self.name.strip().lower()
        else:
            self.name = f"model-{str(uuid.uuid4())}"

    def static_response(self, method) -> JSONResponse:
        """Response from static.

        Args:
            method (str): method http.

        Returns:
            JSONResponse: response.
        """
        content = self.static.get(method)
        if not content:
            content = self.static.get(route_config.HTTPMethod.ALL)
        return JSONResponse(
            status_code=route_config.HTTPMethod.get_status_code(method),
            content=content,
        )


@dataclass(frozen=True)
class ResponseContext:
    """Response Context"""

    errors: Union[list, dict, None] = None
    status_code: int = status.HTTP_200_OK
    save_in_model: bool = False
    model_name: Union[str, None] = None
    model_data: Union[list, dict, None] = None
    content: Union[list, dict, None] = None

    def json_response(self) -> JSONResponse:
        data = self.errors if self.errors else self.content
        return JSONResponse(
            status_code=self.status_code,
            content=data,
        )


@dataclass
class RequestContext:
    """Request Context"""

    method: str
    headers: dict
    body: Any
    original_path: str
    model: Union[Model, None] = None
    features: Feature = field(default_factory=Feature)

    @property
    def path(self) -> str:
        """Get path"""
        p, _ = split_uuid_path(self.original_path)
        return p

    @property
    def resource_id(self) -> str:
        """Get resource id"""
        _, uid = split_uuid_path(self.original_path)
        return uid
