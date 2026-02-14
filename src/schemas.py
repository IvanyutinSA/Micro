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


class ArticleBase(BaseModel):
    pass


class Article(ArticleBase):
    title: str
    description: str
    body: str
    tag_list: list[str]


class CompleteArticle(ArticleBase):
    id: int
    slug: str


class IncompleteCreateArticleRequest(Article):
    slug: str


class CreateArticleRequest(IncompleteCreateArticleRequest):
    user_id: int


class UpdateArticleRequest(Article):
    user_id: int


class DeleteArticleRequest(BaseModel):
    user_id: int
    slug: str


class Comment(BaseModel):
    body: str


class FullComment(Comment):
    id: int
