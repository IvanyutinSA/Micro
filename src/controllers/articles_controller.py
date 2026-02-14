from src.exceptions.http import (NotFoundError,
                                 ForbiddenError,
                                 ConflictError)

from src.schemas import (CreateArticleRequest,
                         Article,
                         UpdateArticleRequest,
                         DeleteArticleRequest)

from src.models.article_model import ArticleModel


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
