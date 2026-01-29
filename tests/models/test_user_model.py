from test_utils.test_suit import TestSuit
from src.models.user_model import UserModel
from src.models.sqlalchemy_db import recreate_tables
from src.schemas import (CreateUserRequest,
                         CreateUserReply,
                         GetUserRequest,
                         GetUserReply)


class TestUserModel(TestSuit):
    def __enter__(self):
        recreate_tables()
        return self

    def test_create(self):
        user_model = UserModel()
        username = "Alice_test_create"
        email = "alice@gmail.com"
        password = "alicesbigsecret"
        request = CreateUserRequest(username=username,
                                    email=email,
                                    password=password)
        expected_reply = CreateUserReply(username=username,
                                         email=email)
        reply = user_model.create(request)

        self.assert_eq(expected_reply, reply)
        self.assert_raises(lambda: user_model(request))

    def test_get_exists(self):
        user_model = UserModel()
        username = "Alice_test_get_exists"
        email = "alice@gmail.com"
        password = "alicesbigsecret"
        request = CreateUserRequest(username=username,
                                    email=email,
                                    password=password)
        user_model.create(request)
        request = GetUserRequest(username=username)
        expected_reply = GetUserReply(username=username,
                                      email=email,
                                      bio=None,
                                      image_url=None)

        reply = user_model.get(request)

        self.assert_eq(expected_reply, reply)

    def test_get_None(self):
        user_model = UserModel()
        username = "Alice_test_get_None"
        request = GetUserRequest(username=username)
        expected_reply = None

        reply = user_model.get(request)

        self.assert_eq(expected_reply, reply)
