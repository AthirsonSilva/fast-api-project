from typing import List, Dict
from uuid import uuid4, UUID

from fastapi import FastAPI

from models import User, Gender, Role

app = FastAPI()

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
async def delete_user(user_id: UUID) -> dict[str, str]:
    for index, user in enumerate(db):
        if user.id == user_id:
            db.pop(index)

            return {"message": "Student deleted successfully!"}

    return {"message": "Student not found!"}


@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: UUID, user: User) -> dict[str, str | User]:
    for index, _user in enumerate(db):
        if _user.id == user_id:
            db[index] = user
            db[index].id = user_id

            return {"message": "Student updated successfully!", "data": user}

    return {"message": "Student not found!"}
