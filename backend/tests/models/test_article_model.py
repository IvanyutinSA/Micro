from test_utils.test_suit import TestSuit
from src.models.article_model import ArticleModel
from src.models.sqlalchemy_db import recreate_tables

from random import randint

from src.schemas import (CreateArticleRequest,
                         Article)


class TestArticleModel(TestSuit):
    def __init__(self):
        self.article_model = ArticleModel()
        self.cache = {}

    def __create_user_id(self, username: str) -> id:
        if username not in self.cache:
            self.cache[username] = randint(0, 2**31-1)
        return self.cache[username]

    def test_create(self):
        user_id = self.__create_user_id("test_create")
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
        user_id = self.__create_user_id("test_get")
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
        user_id = self.__create_user_id("test_update")
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
        user_id = self.__create_user_id("test_delete")
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
