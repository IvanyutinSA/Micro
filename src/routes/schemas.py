from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class User(BaseModel):
    email: str
    username: str
    password: str
    bio: str = ""
    image_url: str = ""


class RegisterRequest(UserBase):
    password: str


class RegisterReply(User):
    username: str


class AuthenticationRequest(UserBase):
    password: str


class UpdateCurrentUserRequest(BaseModel):
    email: str
    bio: str
    image_url: str
