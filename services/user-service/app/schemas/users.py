import uuid
from typing import List
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str = None
    last_name: str = None
    lands: List[int] = []


class UserCreate(schemas.BaseUserCreate):
    first_name: str = None
    last_name: str = None
    lands: List[int] = []


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str = None
    last_name: str = None
    lands: List[int] = []