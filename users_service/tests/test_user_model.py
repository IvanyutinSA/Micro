from test_utils.test_suit import TestSuit
from src.models.user_model import UserModel
from src.models.sqlalchemy_db import recreate_tables
from src.schemas import (
        GetUserRequest,
        GetUserReply,
        CreateUserRequest,
        CreateUserReply,
        UpdateUserRequest,
        UpdateUserReply,
        )


class TestUserModel(TestSuit):
    def __init__(self):
        self.user_model = UserModel()

    def __enter__(self):
        recreate_tables()
        return self

    def __setup_user(self, username: str, test_name: str):
        wrapped_username = f"{test_name}_{username}"
        wrapped_email = f"{username}@{test_name}.com"
        wrapepd_password = f"{username}"
        request = CreateUserRequest(username=wrapped_username,
                                    email=wrapped_email,
                                    password=wrapepd_password)
        _ = self.user_model.create(request)
        return wrapped_username, wrapped_email, wrapepd_password

    def test_update_one_field(self):
        username = "alice"
        username, email, _ = self.__setup_user(username,
                                               "test_update_one_field")
        target_email = "alice@gmail.com"
        self.assert_true(target_email != email)

        field_name = "email"
        user_id = self.user_model.get_full(GetUserRequest(username=username)
                                           ).id

        self.user_model.set_one_field(user_id, field_name, target_email)
        actual_email = self.user_model.get(GetUserRequest(username=username)
                                           ).email

        self.assert_eq(actual_email, target_email)

    def test_get_one_field(self):
        username = "alice"
        username, _, _ = self.__setup_user(username,
                                           "test_get_one_field")
        user_id = self.user_model.get_full(GetUserRequest(username=username)
                                           ).id
        field_name = "username"

        actual_username = self.user_model.get_one_field(user_id, field_name)

        self.assert_eq(actual_username, username)

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

    def test_update_user(self):
        user_model = UserModel()
        username = "Alice_test_update_user"
        email = "alice@gmail.com"
        password = "alicesbigsecret"
        request = CreateUserRequest(username=username,
                                    email=email,
                                    password=password)
        user_model.create(request)
        new_bio = "Rabbit?"
        new_email = "reformed_alice@gmail.com"
        request = UpdateUserRequest(username=username,
                                    password=password,
                                    email=new_email,
                                    bio=new_bio)
        expected_reply = UpdateUserReply(username=username,
                                         password=password,
                                         email=new_email,
                                         bio=new_bio,
                                         image_url=None)

        reply = user_model.update(request)

        self.assert_eq(expected_reply, reply)
