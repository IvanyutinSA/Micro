from pydadntic import BaseModel


class User(BaseModel):
    email: str
    username: str
    password: str
    bio: str = ""
    image_url: str = ""


class RequestRegister(User):
    pass


class RequestAuthenticate(BaseModel):
    username: str
    password: str


class RequestUpdateCurrentUser(User):
    pass
