from pydantic import BaseModel
from typing import Annotated


class UserBase(BaseModel):
    username: str


class User(BaseModel):
    email: str
    username: str
    bio: str | None = None
    image_url: str | None = None


class CreateUserRequest(UserBase):
    email: str
    password: str


class CreateUserReply(User):
    pass


class GetUserRequest(UserBase):
    pass


class GetUserReply(User):
    pass


class AuthenticationRequest(UserBase):
    password: str


class AuthenticationReply(UserBase):
    pass


class UpdateUserRequest(User):
    password: str


class UpdateUserReply(User):
    pass
