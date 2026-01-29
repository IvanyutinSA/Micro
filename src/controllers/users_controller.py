from src.schemas import (
        CreateUserRequest,
        CreateUserReply,
        AuthenticationRequest,
        AuthenticationReply,
        GetUserRequest,
        GetUserReply,
        UpdateUserRequest,
        UpdateUserReply,
)

from src.utilities.general import hash_password
from src.models.user_model import UserModel

user_model = UserModel()


def register_user(request: CreateUserRequest):
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
                      ) -> AuthenticationReply:
    # find user
    user = user_model.get(GetUserRequest(username=request.username))
    if (user is None):
        raise Exception("Incorrect username")
    # check password
    if (user.password != hash_password(request.password)):
        raise Exception("Incorrect password")
    # return good
    reply = AuthenticationReply(username=request.username)
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
    user = user_model.get(GetUserRequest(username=request.username))
    if user is None:
        raise Exception("User is not found")
    reply = user_model.update(request)
    return reply
