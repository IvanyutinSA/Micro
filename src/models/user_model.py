from sqlalchemy.orm import Session
from sqlalchemy import select
from src.schemas import (
        GetUserRequest,
        GetUserReply,
        CreateUserRequest,
        CreateUserReply,
        UpdateUserRequest,
        UpdateUserReply,
        GetUserFullReply,
        )

from src.models.sqlalchemy_models import User

from src.models.sqlalchemy_db import get_engine


class UserModel:
    def __init__(self, engine=None):
        self.engine = engine if engine else get_engine()

    def create(self, request: CreateUserRequest) -> CreateUserReply:
        user = User(username=request.username,
                    hashed_password=request.password,
                    email=request.email)
        with Session(self.engine) as session:
            session.add(user)
            session.commit()
        reply = CreateUserReply(username=request.username,
                                email=request.email)
        return reply

    def get(self, request: GetUserRequest) -> GetUserReply | None:
        user = self.get_full(request)
        reply = None
        if user is not None:
            reply = GetUserReply(username=user.username,
                                 email=user.email,
                                 bio=user.bio,
                                 image_url=user.image_url)
        return reply

    def get_full(self, request: GetUserRequest) -> GetUserFullReply | None:
        username = request.username
        with Session(self.engine) as session:
            user = session.scalars(select(User)
                                   .where(User.username == username)
                                   ).one_or_none()
        reply = None
        if user is not None:
            reply = GetUserFullReply(username=user.username,
                                     password=user.hashed_password,
                                     email=user.email,
                                     bio=user.bio,
                                     image_url=user.image_url,
                                     id=user.id)
        return reply

    def update(self, request: UpdateUserRequest) -> UpdateUserReply:
        with Session(self.engine) as session:
            user = session.scalars(select(User)
                                   .where(User.username == request.username)
                                   ).one()

            user.email = request.email
            user.bio = request.bio
            user.image_url = request.image_url
            user.password = request.password
            session.commit()

            reply = UpdateUserReply(username=user.username,
                                    email=user.email,
                                    bio=user.bio,
                                    image_url=user.image_url)
        return reply
