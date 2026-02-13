from test_utils.test_suit import TestSuit
from src.models.article_model import ArticleModel
from src.models.sqlalchemy_db import recreate_tables
from src.models.user_model import UserModel

from src.schemas import (CreateArticleRequest,
                         Article,
                         CreateUserRequest,
                         GetUserFullReply)


class TestArticleModel(TestSuit):
    def __init__(self):
        self.article_model = ArticleModel()
        self.user_model = UserModel()

    def __create_user(self, username: str) -> GetUserFullReply:
        username = f"TestArticleModel_{username}"
        request = CreateUserRequest(username=username,
                                    email=f"{username}@gmail.com",
                                    password=username)
        self.user_model.create(request)
        return self.user_model.get_full(request)

    def test_create(self):
        user_id = self.__create_user("test_create").id
        slug = "test_create_big_secret"
        title = "Alice's big secret"
        description = "Redacted"
        body = "Redacted"
        tag_list = ["Fiction", "Pizza", "Beef Jerky"]
        request = CreateArticleRequest(user_id=user_id,
                                       slug=slug,
                                       body=body,
                                       tag_list=tag_list,
                                       title=title,
                                       description=description)
        response = self.article_model.create(request)

        self.assert_true(response)

    def test_get(self):
        user_id = self.__create_user("test_get").id
        slug = "test_get_big_secret"
        title = "Alice's big secret"
        description = "Redacted"
        body = "Redacted"
        tag_list = ["Fiction", "Pizza", "Beef Jerky"]
        request = CreateArticleRequest(user_id=user_id,
                                       slug=slug,
                                       body=body,
                                       tag_list=tag_list,
                                       title=title,
                                       description=description)
        response = self.article_model.create(request)
        exp_response = Article(**request.model_dump())

        response = self.article_model.get(slug)
        self.assert_eq(response, exp_response)

    def test_update(self):
        user_id = self.__create_user("test_update").id
        slug = "test_update_big_secret"
        title = "Alice's big secret"
        new_title = "Redacted's big secret"
        description = "Redacted"
        body = "Redacted"
        tag_list = ["Fiction", "Pizza", "Beef Jerky"]
        new_tag_list = ["Fiction", "Redacted", "Redacted", "Extra"]
        request = CreateArticleRequest(user_id=user_id,
                                       slug=slug,
                                       body=body,
                                       tag_list=tag_list,
                                       title=title,
                                       description=description)
        response = self.article_model.create(request)
        request = Article(**request.model_dump())
        request.tag_list = sorted(set(new_tag_list))
        request.title = new_title
        exp_response = request.copy()

        self.article_model.update(request, slug)

        response = self.article_model.get(slug)
        response.tag_list.sort()
        self.assert_eq(response, exp_response)

    def test_delete(self):
        user_id = self.__create_user("test_delete").id
        slug = "test_delete_big_secret"
        title = "Alice's big secret"
        description = "Redacted"
        body = "Redacted"
        tag_list = ["Fiction", "Pizza", "Beef Jerky"]
        request = CreateArticleRequest(user_id=user_id,
                                       slug=slug,
                                       body=body,
                                       tag_list=tag_list,
                                       title=title,
                                       description=description)
        response_create = self.article_model.create(request)
        self.article_model.delete(slug)
        response = self.article_model.get(slug)

        self.assert_eq(response_create, True)
        self.assert_eq(response, None)

    def __enter__(self):
        recreate_tables()
        return self
