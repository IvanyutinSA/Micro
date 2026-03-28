from test_utils.test_suit import TestSuit
from src.models.sqlalchemy_db import recreate_tables
from src.models.user_model import UserModel
from src.models.subscribers_model import SubscribersModel
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
        SubscriptionKey,
        SubscribeRequest
)
from src.controllers.users_controller import (register_user,
                                              authenticate_user,
                                              get_user,
                                              update_user,
                                              get_subscription_key,
                                              set_subscription_key,
                                              subscribe)


class TestUserController(TestSuit):
    def __enter__(self):
        recreate_tables()
        return self

    def __init__(self):
        self.user_model = UserModel()
        self.sub_model = SubscribersModel()

    def __setup_user(self, username: str, test_name: str):
        wrapped_username = f"{test_name}_{username}"
        wrapped_email = f"{username}@{test_name}.com"
        wrapepd_password = f"{username}"
        request = CreateUserRequest(username=wrapped_username,
                                    email=wrapped_email,
                                    password=wrapepd_password)
        _ = self.user_model.create(request)
        return wrapped_username, wrapped_email, wrapepd_password

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

    def test_set_get_subscription_key(self):
        username = "alice"
        username, _, _ = self.__setup_user(username,
                                           "test_set_subscription_key")
        user_id = self.user_model.get_full(GetUserRequest(username=username)
                                           ).id

        sub_key = SubscriptionKey(subscription_key="sub_key")
        set_subscription_key(sub_key, user_id)

        getted_sub_key = get_subscription_key(user_id)
        actual_sub_key = self.user_model.get_one_field(user_id,
                                                       "subscription_key")

        self.assert_eq(sub_key, getted_sub_key)
        self.assert_eq(sub_key.subscription_key, actual_sub_key)

    def test_subscribe(self):
        username = "alice"
        username, _, _ = self.__setup_user(username,
                                           "test_subscribe")
        user_id = self.user_model.get_full(GetUserRequest(username=username)
                                           ).id
        auth_id = 1
        request = SubscribeRequest(target_user_id=auth_id)
        subscribe(user_id, request)

        sub_ids = self.sub_model.get_by_auth_id(auth_id).sub_ids
        self.assert_true(user_id in sub_ids)
