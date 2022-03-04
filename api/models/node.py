import ast
from datetime import datetime
from typing import Optional
from uuid import UUID
from uuid import uuid4

from fastapi import status
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from api.configs import app_configs
from api.utils.errors import custom_http_exception
from api.validators import validate


class Node(BaseModel):
    """Validation when creating node.

    Args:
        BaseModel: BaseModel of pydantic.

    Raises:
        custom_http_exception: Custom exception http with error json.
    """

    reference_id: UUID = Field(default_factory=uuid4, alias="reference_id")
    path: str
    schema_name: dict = Field(alias="schema")
    model_name: str = Field(alias="model", max_length=100)

    is_active: bool = True
    created_at: Optional[datetime] = datetime.now()

    class Config:
        """Config of class Node"""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    @validator("model_name")
    def name_model_name(cls, v) -> str:
        """Validate model name.

        Args:
            v (str): Model name.

        Raises:
            ValueError: error when validating model name.

        Returns:
            str: Model name.
        """
        m = v.strip()
        if not m.isalpha():
            raise ValueError("the model only allows letters without spaces.")
        return m

    @validator("schema_name")
    def name_schema_name(cls, v) -> dict:
        """Validate schema.

        Args:
            v (dict): Schema.

        Raises:
            ValueError: error when validating schema.

        Returns:
            dict: schema.
        """
        r = validate.schema(v)
        if r:
            raise custom_http_exception(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                loc=["body", "model"],
                msg="errors in the validation of the schema.",
                type_name="schema",
                errors=ast.literal_eval(str(r)),
            )
        return v

    @validator("path")
    def name_path(cls, v):
        """Validate path name.

        Args:
            v (str): Path name.

        Raises:
            ValueError: error when validating path name.

        Returns:
            str: Path name.
        """
        p = v.strip()
        if not p.startswith("/"):
            raise ValueError("the path must start with the '/' character.")

        if len(p.split("/")) == 1:
            return "/"

        for row in p.split("/"):
            if not cls._validate_path_row(cls, row):
                raise ValueError(
                    "the path must only contain letters and the '/' character."
                )
        path_modified = p[:-1] if p.endswith("/") else p
        if len(path_modified.split("/")) > app_configs.PATH_SECTION:
            raise ValueError(
                f"Only one path with a maximum of {app_configs.PATH_SECTION - 1} "
                "sections is allowed."
            )
        return p

    def _validate_path_row(cls, v) -> bool:
        if v.isalpha() or v == "":
            return True
        return False
