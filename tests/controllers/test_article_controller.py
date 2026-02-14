from test_utils.test_suit import TestSuit
from src.models.sqlalchemy_db import recreate_tables
from src.controllers.articles_controller import ArticleController
from src.models.user_model import UserModel
from src.schemas import (CreateArticleRequest,
                         CreateUserRequest,
                         GetUserFullReply,
                         Article,
                         UpdateArticleRequest,
                         DeleteArticleRequest)


class TestArticleController(TestSuit):
    def __enter__(self):
        recreate_tables()
        return self

    def __init__(self):
        self.controller = ArticleController()
        self.user_model = UserModel()

    def __create_user(self, username: str) -> GetUserFullReply:
        username = f"TestArticleModel_{username}"
        request = CreateUserRequest(username=username,
                                    email=f"{username}@gmail.com",
                                    password=username)
        self.user_model.create(request)
        return self.user_model.get_full(request)

    def test_create_article(self):
        user_id = self.__create_user("test_create_article").id
        slug = "test_create_article_big_secret"
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
        self.controller.create_article(request)
        self.controller.get_article_by_slug(slug)

    def test_get_articles(self):
        user_id = self.__create_user("test_get_articles").id
        slug = "test_get_articles_1"
        title = "test_get_articles_1"
        title2 = "test_get_articles_2"
        description = "Redacted"
        body = "Redacted"
        tag_list = ["Fiction", "Pizza", "Beef Jerky"]
        request = CreateArticleRequest(user_id=user_id,
                                       slug=slug,
                                       body=body,
                                       tag_list=tag_list,
                                       title=title,
                                       description=description)
        self.controller.create_article(request)
        request = CreateArticleRequest(user_id=user_id,
                                       slug="test_get_articles_ok",
                                       body=body,
                                       tag_list=tag_list,
                                       title=title2,
                                       description=description)
        self.controller.create_article(request)
        articles = self.controller.get_articles()
        counter = 0
        for article in articles:
            if article.title in [title, title2]:
                counter += 1
        self.assert_true(counter > 1)

    def test_get_article_by_slug(self):
        user_id = self.__create_user("test_get_article_by_slug").id
        slug = "test_get_article_by_slug"
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
        self.controller.create_article(request)
        response = self.controller.get_article_by_slug(slug)

        request.tag_list.sort()
        exp_response = Article(**request.model_dump())
        response.tag_list.sort()

        self.assert_eq(response, exp_response)
        self.assert_raises(lambda _: self.test_get_article_by_slug(
            "test_get_article_by_slug_non_existen"))

    def test_update_article(self):
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
        response = self.controller.create_article(request)
        request = UpdateArticleRequest(**request.model_dump())
        request.tag_list = sorted(set(new_tag_list))
        request.title = new_title
        exp_response = Article(**request.model_dump())

        self.controller.update_article(request, slug)

        response = self.controller.get_article_by_slug(slug)
        response.tag_list.sort()
        self.assert_eq(response, exp_response)

        request_forbidden = UpdateArticleRequest(**request.model_dump())
        request_forbidden.user_id = 999
        self.assert_raises(lambda: self.controller.update_article(
            request_forbidden, slug))

        request_not_found = UpdateArticleRequest(**request.model_dump())
        slug_not_found = "test_update_article_definitly_not_found"
        self.assert_raises(lambda _: self.controller.update_article(
            request_not_found, slug_not_found))

    def test_delete_article(self):
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
        self.controller.create_article(request)
        request_positive = DeleteArticleRequest(user_id=user_id,
                                                slug=slug)

        self.controller.delete_article(request_positive)

        self.assert_raises(lambda: self.controller.get_article_by_slug(slug))

        request_not_found = DeleteArticleRequest(user_id=user_id,
                                                 slug=slug)
        self.assert_raises(lambda: self.controller.delete_article(
            request_not_found))

        self.controller.create_article(request)
        request_forbidden = DeleteArticleRequest(user_id=999,
                                                 slug=slug)
        self.assert_raises(lambda: self.controller.delete_article(
            request_forbidden))
