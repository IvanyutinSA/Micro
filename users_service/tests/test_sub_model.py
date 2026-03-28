from src.models.subscribers_model import SubscribersModel
from test_utils.test_suit import TestSuit
from src.models.sqlalchemy_db import recreate_tables


class TestSubscribersModel(TestSuit):
    def __enter__(self):
        recreate_tables()
        return self

    def __init__(self):
        self.sub_model = SubscribersModel()

    def test_create(self):
        sub_ids = [1, 2, 3]
        auth_id = 69

        for sub_id in sub_ids:
            self.sub_model.create(sub_id, auth_id)
        actual_sub_ids = self.sub_model.get_by_auth_id(auth_id).sub_ids

        self.assert_eq(actual_sub_ids, sub_ids)
