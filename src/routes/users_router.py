from fastapi import APIRouter
from src.controllers.users_controller import UserController
from src.routes.schemas import (
        RegisterRequest, RegisterReply)


router = APIRouter(prefix="/users")
controller = UserController()


@router.post("/")
def register(request: RegisterRequest):
    reply = controller.register(request)
    reply = RegisterReply()
    return reply


@router.post("/login")
def authenticate():
    pass


@router.get("/")
def get_current_user():
    pass


@router.put("/")
def update_current_user():
    pass
