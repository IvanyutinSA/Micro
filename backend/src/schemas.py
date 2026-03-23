from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


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
