from test_utils.test_suit import TestSuit
from src.models.sqlalchemy_db import recreate_tables
from src.models.user_model import UserModel
from src.models.article_model import ArticleModel 

from src.controllers.comments_controller import CommentController

from src.schemas import (GetUserFullReply,
                         CreateUserRequest,
                         CompleteArticle,
                         CreateArticleRequest,
                         Comment,
                         FullComment)


class TestCommentController(TestSuit):
    def __enter__(self):
        recreate_tables()
        return self

    def __init__(self):
        self.comment_controller = CommentController()
        self.article_model = ArticleModel()
        self.user_model = UserModel()

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

    def test_post_comment(self):
        user = self.__create_user("test_post_comment")
        article = self.__create_article("test_post_comment", user.id)
        body = "she's my horror queen"

        request = Comment(body=body)
        self.comment_controller.post_comment(request, article.slug, user.id)
        raises_f = lambda: self.comment_controller.post_comment(
                request, "NONSENSE", user.id)

        self.assert_raises(raises_f)

    def test_get_comments(self):
        user = self.__create_user("test_get_comments")
        article = self.__create_article("test_get_comments", user.id)
        body1 = "she's my graveyard baby"
        body2 = "she's my horror queen"

        request1 = Comment(body=body1)
        request2 = Comment(body=body2)

        self.comment_controller.post_comment(request1, article.slug, user.id)
        self.comment_controller.post_comment(request2, article.slug, user.id)

        comments = self.comment_controller.get_comments(article.slug)

        bodies = [comment.body for comment in comments]

        self.assert_true(body1 in bodies)
        self.assert_true(body2 in bodies)

        comments = self.comment_controller.get_comments("NONSENSE")

        self.assert_eq(len(comments), 0)

    def test_delete_comment(self):
        user = self.__create_user("test_delete_comment")
        article = self.__create_article("test_delete_comment", user.id)
        body = "she's my graveyard baby"

        request = Comment(body=body)
        self.comment_controller.post_comment(request, article.slug, user.id)
        comment = self.comment_controller.get_comments(article.slug)[0]
        self.comment_controller.delete_comment(article.slug,
                                               comment.id,
                                               user.id)

        comments = self.comment_controller.get_comments(article.slug)
        self.assert_eq(len(comments), 0)

        self.assert_raises(lambda: self.comment_controller.delete_comment(
            article.slug, comment.id, user.id))

        self.assert_raises(lambda: self.comment_controller.delete_comment(
            article.slug, 999, user.id))

        self.assert_raises(lambda: self.comment_controller.delete_comment(
            article.slug, comment.id, 999))
