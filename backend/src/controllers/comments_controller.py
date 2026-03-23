from src.exceptions.http import (ForbiddenError,
                                 NotFoundError)
from src.models.comment_model import CommentModel
from src.schemas import Comment, FullComment


class CommentController:
    def __init__(self):
        self.comment_model = CommentModel()

    def post_comment(self,
                     request: Comment,
                     slug: str,
                     user_id: int):
        result = self.comment_model.create(request, slug, user_id)
        if not result:
            raise NotFoundError("Article not found")

    def get_comments(self, slug: str) -> list[FullComment]:
        return self.comment_model.get(slug)

    def delete_comment(self, slug: str, comment_id: int, user_id: int):
        if not self.comment_model.is_owned_by_user(user_id, comment_id):
            raise ForbiddenError()
        if not self.comment_model.delete(comment_id):
            raise NotFoundError()
