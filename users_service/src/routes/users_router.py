from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.routes.extra import get_current_user_req, get_current_user_id
from src.controllers.users_controller import (
        register_user,
        authenticate_user,
        get_user,
        update_user,
        subscribe,
        get_subscription_key,
        set_subscription_key as uc_set_subscription_key
)

from src.schemas import (
        CreateUserRequest,
        CreateUserReply,
        GetUserRequest,
        GetUserReply,
        UpdateCurrentUserRequest,
        UpdateUserRequest,
        UpdateUserReply,
        Token,
        SubscriptionKey,
        SubscribeRequest,
)


router = APIRouter()


@router.post("/")
def register(request: CreateUserRequest) -> CreateUserReply:
    return register_user(request)


@router.post("/login")
def authenticate(request: Annotated[OAuth2PasswordRequestForm, Depends()]
                 ) -> Token:
    return authenticate_user(request)


@router.get("/")
def get_current_user(request: Annotated[GetUserRequest,
                                        Depends(get_current_user_req)]
                     ) -> GetUserReply:
    return get_user(request)


@router.put("/")
def update_current_user(request: UpdateCurrentUserRequest,
                        get_user_req: Annotated[GetUserRequest,
                                                Depends(get_current_user_req)]
                        ) -> UpdateUserReply:
    request = UpdateUserRequest(username=get_user_req.username,
                                password=request.password,
                                email=request.email,
                                image_url=request.image_url,
                                bio=request.bio)
    return update_user(request)


@router.put("/me/subscription-key")
def set_subscription_key(request: SubscriptionKey,
                         user_id: Annotated[int,
                                            Depends(get_current_user_id)]
                         ):
    uc_set_subscription_key(request, user_id)


@router.put("/subscribe")
def subscribe_user(request: SubscribeRequest,
                   user_id: Annotated[int,
                                      Depends(get_current_user_id)]
                   ):
    subscribe(user_id, request)
