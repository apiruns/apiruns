from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, Field
from app.api.utils import mongo

class Node(BaseModel):
    id: mongo.PyObjectId = Field(default_factory=mongo.PyObjectId, alias="_id", hidden_from_schema=True)
    path: str
    structure: dict
    algo: str

    is_active: bool = True
    created_at: Optional[datetime] = datetime.now()


    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {mongo.ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
            }
        }
