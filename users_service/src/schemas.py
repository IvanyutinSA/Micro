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


class GetUserFullReply(User):
    id: int
    password: str


class AuthenticationRequest(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UpdateUserRequest(User):
    password: str | None = None


class UpdateCurrentUserRequest(UpdateUserRequest):
    username: str | None = None


class UpdateUserReply(User):
    pass


class SubscriptionKey(BaseModel):
    subscription_key: str | None


class SubscribeRequest(BaseModel):
    target_user_id: int


class Subscribers(BaseModel):
    sub_ids: list[int]
