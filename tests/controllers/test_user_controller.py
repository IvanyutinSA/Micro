from test_utils.test_suit import TestSuit
from src.models.sqlalchemy_db import recreate_tables
from src.utilities.jwt import verify_token, decode_token
from src.schemas import (
        CreateUserRequest,
        CreateUserReply,
        AuthenticationRequest,
        Token,
        GetUserRequest,
        GetUserReply,
        UpdateUserRequest,
        UpdateUserReply,
)
from src.controllers.users_controller import (register_user,
                                              authenticate_user,
                                              get_user,
                                              update_user)


class TestUserController(TestSuit):
    def __enter__(self):
        recreate_tables()
        return self

    def test_register(self):
        username = "Alice_test_register"
        email = "alice@gmail.com"
        password = "alicesbigsecret"
        request = CreateUserRequest(username=username,
                                    email=email,
                                    password=password)
        expected_reply = CreateUserReply(username=username,
                                         email=email)
        reply = register_user(request)

        self.assert_eq(expected_reply, reply)

    def test_authenticate_correct_data(self):
        username = "Alice_test_authenticate_correct_data"
        password = "alicesbigsecret"
        email = "alice@gmail.com"
        request = CreateUserRequest(username=username,
                                    email=email,
                                    password=password)
        register_user(request)
        request = AuthenticationRequest(username=username,
                                        password=password)
        expected_token_type = "bearer"

        reply = authenticate_user(request)

        self.assert_eq(reply.token_type, expected_token_type)
        self.assert_true(verify_token(reply.access_token))
        self.assert_eq(decode_token(reply.access_token)['sub'], username)

    def test_authenticate_wrong_username(self):
        username = "Alice_test_authenticate_wrong_username"
        password = "alicesbiggestsecret"
        request = AuthenticationRequest(username=username,
                                        password=password)
        self.assert_raises(lambda: authenticate_user(request))

    def test_authenticate_wrong_password(self):
        username = "Alice_test_authenticate_wrong_password"
        password = "alicesbiggestsecret"
        wrong_password = "why?"
        email = "alice@gmail.com"
        request = CreateUserRequest(username=username,
                                    email=email,
                                    password=password)
        register_user(request)
        request = AuthenticationRequest(username=username,
                                        password=wrong_password)

        self.assert_raises(lambda: authenticate_user(request))

    def test_get_user_existing(self):
        username = "Alice_test_get_user_existing"
        password = "alicesbiggestsecret"
        email = "alice@gmail.com"
        request = CreateUserRequest(username=username,
                                    email=email,
                                    password=password)
        register_user(request)
        request = GetUserRequest(username=username)
        expected_reply = GetUserReply(username=username,
                                      email=email)

        reply = get_user(request)

        self.assert_eq(expected_reply, reply)

    def test_get_user_non_existing(self):
        username = "Alice_test_get_user_non_existing"
        request = GetUserRequest(username=username)

        self.assert_raises(lambda: get_user(request))

    def test_update_user(self):
        username = "Alice_test_update_user"
        password = "alicesbiggestsecret"
        email = "alice@gmail.com"
        new_bio = "Rabit?"
        request = CreateUserRequest(username=username,
                                    email=email,
                                    password=password)
        register_user(request)
        request = UpdateUserRequest(username=username,
                                    email=email,
                                    bio=new_bio)
        expected_reply = UpdateUserReply(username=username,
                                         email=email,
                                         bio=new_bio)

        reply = update_user(request)

        self.assert_eq(expected_reply, reply)

    def test_update_user_non_existing(self):
        username = "Alicetest_update_user_non_existing"
        email = "alice@gmail.com"
        new_bio = "Rabit?"
        request = UpdateUserRequest(username=username,
                                    email=email,
                                    bio=new_bio)

        self.assert_raises(lambda: update_user(request))
