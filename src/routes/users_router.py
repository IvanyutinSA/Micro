from fastapi import APIRouter
from src.controllers.users_controller import (
        register_user,
        authenticate_user,
        get_user,
        update_user,
)

from src.schemas import (
        CreateUserRequest,
        CreateUserReply,
        AuthenticationRequest,
        AuthenticationReply,
        GetUserReply,
        UpdateUserRequest,
        UpdateUserReply,
)


router = APIRouter(prefix="/users")


@router.post("/")
def register(request: CreateUserRequest) -> CreateUserReply:
    return register_user(request)


@router.post("/login")
def authenticate(request: AuthenticationRequest) -> AuthenticationReply:
    return authenticate_user(request)


@router.get("/")
def get_current_user(request) -> GetUserReply:
    return get_user(request)


@router.put("/")
def update_current_user(request: UpdateUserRequest
                        ) -> UpdateUserReply:
    return update_user(request)
