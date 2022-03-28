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


@dataclass
class BaseModel:
    """Field bases"""

    public_id: str = str(uuid.uuid4())
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = None
    deleted_at: datetime = None

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


@dataclass
class APIResponse:
    """Response Object"""

    content: Union[list, dict]
    status_code: int = status.HTTP_200_OK

    def json(self) -> JSONResponse:
        """Return JsonResponse.

        Returns:
            JSONResponse: json with content and status code.
        """
        return JSONResponse(status_code=self.status_code, content=self.content)


@dataclass(frozen=True)
class ResponseContext:

    errors: Union[list, dict] = None
    status_code: int = status.HTTP_200_OK
    save_in_model: bool = False
    model_name: str = None
    model_data: Union[list, dict] = None
    content: Union[list, dict] = None

    def json_response(self):
        return APIResponse(content=self.content, status_code=self.status_code)


@dataclass(frozen=True)
class InputContext:

    model: dict
    method: str
    headers: dict
    body: Any
