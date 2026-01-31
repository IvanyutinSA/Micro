from src.utilities.jwt import create_access_token
from src.schemas import (
        CreateUserRequest,
        CreateUserReply,
        AuthenticationRequest,
        Token,
        GetUserRequest,
        GetUserReply,
        UpdateUserRequest,
        UpdateUserReply,
)

from src.utilities.general import hash_password
from src.models.user_model import UserModel

user_model = UserModel()


def register_user(request: CreateUserRequest
                  ) -> CreateUserReply:
    # find user
    user = user_model.get(GetUserRequest(username=request.username))
    if user is not None:
        raise Exception("User already exists")
    # hash password
    request.password = hash_password(request.password)
    # add to db
    reply = user_model.create(request)
    return reply


def authenticate_user(request: AuthenticationRequest
                      ) -> Token:
    user = user_model.get_full(GetUserRequest(username=request.username))
    if (user is None):
        raise Exception("Incorrect username")
    if (user.password != hash_password(request.password)):
        raise Exception("Incorrect password")
    token = create_access_token(request.username)
    reply = Token(access_token=token,
                  token_type="bearer")
    return reply


def get_user(request: GetUserRequest) -> GetUserReply:
    # find user
    reply = user_model.get(request)
    if (reply is None):
        raise Exception("User is not found")
    # return
    return reply


def update_user(request: UpdateUserRequest) -> UpdateUserReply:
    # find user
    user = user_model.get_full(GetUserRequest(username=request.username))
    if user is None:
        raise Exception("User is not found")

    if request.password:
        request.password = hash_password(request.password)
    else:
        request.password = user.password

    reply = user_model.update(request)
    return reply
