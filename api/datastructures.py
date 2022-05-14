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

from api.utils.common import json_serial
from api.utils.common import split_uuid_path


@dataclass
class BaseModel:
    """Field bases"""

    public_id: str = str(uuid.uuid4())
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> dict:
        return json.loads(
            json.dumps(self.to_dict(), indent=4, sort_keys=False, default=json_serial)
        )


@dataclass
class Model(BaseModel):
    """Admin Model"""

    path: str = "/"
    model: str = f"model_{str(uuid.uuid4())}"
    schema: dict = field(default_factory=dict)

    def __post_init__(self):
        self.model = self.model.strip().lower()
        self.path = self.path.strip().lower()


@dataclass(frozen=True)
class ResponseContext:

    errors: Union[list, dict, None] = None
    status_code: int = status.HTTP_200_OK
    save_in_model: bool = False
    model_name: Union[str, None] = None
    model_data: Union[list, dict, None] = None
    content: Union[list, dict, None] = None

    def json_response(self):
        data = self.errors if self.errors else self.content
        return JSONResponse(
            status_code=self.status_code,
            content=data,
        )


@dataclass(frozen=True)
class InputContext:

    model: dict
    method: str
    headers: dict
    body: Any
    original_path: str

    @property
    def path(self):
        p, _ = split_uuid_path(self.original_path)
        return p

    @property
    def resource_id(self):
        _, uid = split_uuid_path(self.original_path)
        return uid
