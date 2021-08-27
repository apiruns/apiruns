from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from pydantic import BaseModel, Field
from api.utils import mongo



class Node(BaseModel):
    reference_id: UUID = Field(default_factory=uuid4, alias="id")
    path: str
    schema_name: dict = Field(alias="schema")
    model_name: str = Field(alias="model")

    is_active: bool = True
    created_at: Optional[datetime] = datetime.now()


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {}
