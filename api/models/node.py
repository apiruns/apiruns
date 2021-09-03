from datetime import datetime
from uuid import UUID, uuid4
import ast
from typing import Optional
from pydantic import BaseModel, Field, validator
from api.utils import mongo
from api.validators import validate
from fastapi import status
from api.utils.errors import custom_http_exception

class Node(BaseModel):
    reference_id: UUID = Field(default_factory=uuid4, alias="id")
    path: str
    schema_name: dict = Field(alias="schema")
    model_name: str = Field(alias="model", max_length=100)

    is_active: bool = True
    created_at: Optional[datetime] = datetime.now()


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {}

    @validator('model_name')
    def name_model_name(cls, v):
        if not v.isalpha() or " " in v:
            raise ValueError('the model only allows letters without spaces.')
        return v

    @validator('schema_name')
    def name_schema_name(cls, v):
        r = validate.schema(v)
        if r:
            raise custom_http_exception(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                loc=["body", "model"],
                msg="errors in the validation of the schema.",
                type_name="schema",
                errors=ast.literal_eval(str(r))
            )
        return v
