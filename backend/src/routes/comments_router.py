from typing import Annotated
from fastapi import APIRouter, Depends
from src.schemas import Comment, FullComment
from src.routes.extra import get_current_user_id
from src.controllers.comments_controller import CommentController

router = APIRouter(prefix="/articles")
controller = CommentController()


@router.post("/{slug}/comments")
def post_comment(request: Comment,
                 slug: str,
                 user_id: Annotated[int,
                                    Depends(get_current_user_id)]):
    controller.post_comment(request, slug, user_id)


@router.get("/{slug}/comments")
def get_comments(slug: str) -> list[FullComment]:
    return controller.get_comments(slug)


@router.delete("/{slug}/comments/{id}")
def delete_comment(slug: str,
                   id: int,
                   user_id: Annotated[int,
                                      Depends(get_current_user_id)]):
    controller.delete_comment(slug, id, user_id)
