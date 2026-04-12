from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    # Covert modelos SQLAlchemy para modelo Pydantic
    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    # deve ser int e  maior ou igual à 0
    offset: Annotated[int, Field(default=0, ge=0)]
    limit: Annotated[int, Field(default=100, ge=1)]

    # é o mesmo que:
    # limit: int = Field(default=100, ge=1)
