from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class Todo(BaseModel):
    title : str
    status : str


class TodoRead(Todo):
    # Enable ORM mode so FastAPI can serialize SQLAlchemy model instances
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at : datetime
    updated_at : datetime


class TodoPatch(BaseModel):
    # These properties are optional to comply with partial update
    # on PATCH request and can be ommitted
    title: Optional[str] = None
    status: Optional[str] = None


class TodoDelete(BaseModel):
    id: int