from typing import Annotated
from fastapi import APIRouter, Depends

from src.schemas import (Article, CreateArticleRequest,
                         IncompleteCreateArticleRequest,
                         UpdateArticleRequest, DeleteArticleRequest)
from src.routes.extra import get_current_user_id
from src.controllers.articles_controller import ArticleController


controller = ArticleController()

router = APIRouter(prefix="/articles")


@router.post("/")
def create_article(request: IncompleteCreateArticleRequest,
                   user_id: Annotated[int,
                                      Depends(get_current_user_id)]):
    request = CreateArticleRequest(user_id=user_id,
                                   **request.model_dump())
    controller.create_article(request)


@router.get("/")
def get_articles() -> list[Article]:
    return controller.get_articles()


@router.get("/{slug}")
def get_article_by_slug(slug: str) -> Article:
    return controller.get_article_by_slug(slug)


@router.put("/{slug}")
def update_article(slug: str,
                   request: Article,
                   user_id: Annotated[int,
                                      Depends(get_current_user_id)]
                   ):
    request = UpdateArticleRequest(slug=slug,
                                   user_id=user_id,
                                   **request.model_dump())
    controller.update_article(request, slug)


@router.delete("/{slug}")
def delete_article(slug: str,
                   user_id: Annotated[int,
                                      Depends(get_current_user_id)]):
    request = DeleteArticleRequest(slug=slug,
                                   user_id=user_id)
    controller.delete_article(request)


@router.post("/{id}/publish")
def publish(id: int,
            user_id: Annotated[int,
                               Depends(get_current_user_id)]):
    controller.publish(id, user_id)


@router.post("/{id}/reject")
def reject(id: int):
    controller.reject(id)
