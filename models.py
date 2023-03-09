from typing import Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel
from enum import Enum


class Gender(str, Enum):
    male = "Male"
    female = "Female"


class Role(str, Enum):
    admin = "Admin"
    user = "User"
    student = "Student"


class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: Gender
    roles: List[Role]
