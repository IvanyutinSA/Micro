import os
import redis

from src.exceptions.http import (NotFoundError,
                                 ForbiddenError,
                                 ConflictError)

from celery import Celery
from dotenv import load_dotenv

from src.schemas import (CreateArticleRequest,
                         Article,
                         UpdateArticleRequest,
                         DeleteArticleRequest)

from src.models.article_model import ArticleModel

load_dotenv()
celery = Celery("worker", broker=os.getenv("REDIS_URL"))


class ArticleController:
    def __init__(self):
        self.article_model = ArticleModel()

    def create_article(self, request: CreateArticleRequest):
        if self.article_model.get(request.slug) is not None:
            raise ConflictError("Try another slug")
        self.article_model.create(request)

    def get_articles(self) -> list[Article]:
        return self.article_model.get_all()

    def get_article_by_slug(self, slug: str) -> Article:
        response = self.article_model.get(slug)
        if response is None:
            raise NotFoundError()
        return response

    def update_article(self, request: UpdateArticleRequest, slug: str):
        user_id = request.user_id
        if not self.article_model.is_user_own_article_by_slug(user_id, slug):
            raise ForbiddenError()
        self.article_model.update(Article(**request.model_dump()), slug)

    def delete_article(self, request: DeleteArticleRequest):
        user_id = request.user_id
        slug = request.slug
        if not self.article_model.is_user_own_article_by_slug(user_id, slug):
            raise ForbiddenError()
        if not self.article_model.delete(slug):
            raise NotFoundError()

    def publish(self, article_id: int, author_id: int):
        # check if its indeed author
        slug = self.article_model.get_one_field_by_id(article_id, "slug")
        if not self.article_model.is_user_own_article_by_slug(author_id,
                                                              slug):
            raise ForbiddenError()
        # set status to pending
        status = "PENDING_STATUS"
        self.article_model.set_one_field(article_id, "status", status)
        title = self.article_model.get_one_field_by_id(article_id, "title")
        body = self.article_model.get_one_field_by_id(article_id, "body")
        args = [article_id, author_id, title, body, author_id]
        celery.send_task("post.moderate", args)

    def reject(self, article_id: int):
        self.article_model.set_one_field(article_id, "status", "REJECTED")

    def set_status(self, article_id: int, status: str):
        self.article_model.set_one_field(article_id, "status", status)
