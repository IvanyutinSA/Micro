from test_utils.test_suit import TestSuit
from src.models.sqlalchemy_db import recreate_tables
from src.models.user_model import UserModel
from src.models.article_model import ArticleModel 
from src.models.comment_model import CommentModel

from src.schemas import (GetUserFullReply,
                         CreateUserRequest,
                         CreateArticleRequest,
                         Comment,
                         FullComment,
                         CompleteArticle)


class TestCommentModel(TestSuit):
    def __enter__(self):
        recreate_tables()
        return self

    def __init__(self):
        self.user_model = UserModel()
        self.article_model = ArticleModel()
        self.comment_model = CommentModel()

    def __create_user(self, username: str) -> GetUserFullReply:
        username = f"TestArticleModel_{username}"
        request = CreateUserRequest(username=username,
                                    email=f"{username}@gmail.com",
                                    password=username)
        self.user_model.create(request)
        return self.user_model.get_full(request)

    def __create_article(self, name: str, user_id: int) -> CompleteArticle:
        user_id = user_id
        slug = f"{user_id}:{name}"
        title = name
        description = name
        body = name
        tag_list = []
        request = CreateArticleRequest(user_id=user_id,
                                       slug=slug,
                                       title=title,
                                       description=description,
                                       body=body,
                                       tag_list=tag_list)
        self.article_model.create(request)
        return self.article_model.get_complete(slug)

    def test_create(self):
        user = self.__create_user("Alice")
        article = self.__create_article("Alices_big_secret", user.id)
        body = "she's my graveyard baby"
        request = Comment(body=body)

        response = self.comment_model.create(request, article.slug, user.id)

        self.assert_eq(response, True)

    def test_get(self):
        user = self.__create_user("test_get_Alice")
        article = self.__create_article("test_get_Alices_big_secret",
                                        user.id)
        body = "she's my graveyard baby"
        request = Comment(body=body)

        self.comment_model.create(request, article.slug, user.id)
        comments = self.comment_model.get(article.slug)

        self.assert_eq(len(comments), 1)

    def test_delete(self):
        user = self.__create_user("test_delete_Alice")
        article = self.__create_article("test_delete_Alices_big_secret",
                                        user.id)
        body = "she's my graveyard baby"
        request = Comment(body=body)
        self.comment_model.create(request, article.slug, user.id)

        exp_comments = self.comment_model.get(article.slug)
        comment = exp_comments.pop()

        self.assert_eq(self.comment_model.delete(comment.id), 1)
        comments = self.comment_model.get(article.slug)

        self.assert_eq(comments, exp_comments)
