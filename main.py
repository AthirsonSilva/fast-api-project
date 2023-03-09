from typing import List, Dict, Optional
from uuid import uuid4, UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models import User, Gender, Role

app = FastAPI()


class UserUpdateDto(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    roles: Optional[List[Role]] = None


db: List[User] = [
    User(
        id=UUID("56a6250f-eabb-4c46-875f-8f3298ae7bf6"),
        first_name="John",
        last_name="Doe",
        middle_name="Smith",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
    ),
    User(
        id=UUID("da4726ca-164e-406c-af39-da5e53244f81"),
        first_name="Mary",
        last_name="Doe",
        middle_name="Smith",
        gender=Gender.female,
        roles=[Role.user],
    ),
    User(
        id=UUID("5cb37849-0c8d-40b4-99a9-ddc3ca184600"),
        first_name="Gregory",
        last_name="Doe",
        middle_name="Rose",
        gender=Gender.male,
        roles=[Role.student],
    ),
]


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.get("/api/v1/users")
async def fetch_users() -> dict[str, str | list[User]]:
    return {"message": "Students fetched successfully!", "data": db}


@app.post("/api/v1/users")
async def create_user(user: User) -> dict[str, str | User]:
    db.append(user)

    return {"message": "Student created successfully!", "data": user}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for index, user in enumerate(db):
        if user.id == user_id:
            db.pop(index)

            return {"message": "Student deleted successfully!"}

    return HTTPException(status_code=404, detail="Student not found!", headers={"X-Error": "There goes my error"})


@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: UUID, user: UserUpdateDto):
    for index, _user in enumerate(db):
        if _user.id == user_id:
            if user.first_name is not None:
                db[index].first_name = user.first_name

            if user.last_name is not None:
                db[index].last_name = user.last_name

            if user.middle_name is not None:
                db[index].middle_name = user.middle_name

            if user.roles is not None:
                db[index].roles = user.roles

            return {"message": "Student updated successfully!", "data": user}

    return HTTPException(status_code=404, detail="Student not found!", headers={"X-Error": "There goes my error"})


@app.get("/api/v1/users/{user_id}")
async def fetch_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            return {"message": "Student fetched successfully!", "data": user}

    return HTTPException(status_code=404, detail="Student not found!", headers={"X-Error": "There goes my error"})
