from typing import Annotated
from fastapi import APIRouter, Depends

from src.schemas import Article, CreateArticleRequest, GetUserRequest
from src.routes.extra import get_current_user_req


router = APIRouter(prefix="/articles")


@router.post("/")
def create_article(request, user: Annotated[GetUserRequest,
                                            Depends(get_current_user_req)]):
    pass


@router.get("/")
def get_articles() -> list[Article]:
    pass


@router.get("/{slug}")
def get_article_by_slug(slug: str) -> Article:
    pass


@router.put("/{slug}")
def update_article(slug: str,
                   request: Article,
                   user: Annotated[GetUserRequest,
                                   Depends(get_current_user_req)]
                   ) -> Article:
    pass


@router.delete("/{slug}")
def delete_article(slug: str):
    pass
