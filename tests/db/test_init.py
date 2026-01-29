from test_utils.test_suit import TestSuit
from src.models.sqlalchemy_db import get_engine, recreate_tables
from src.models.sqlalchemy_models import User
from sqlalchemy.orm import Session
from sqlalchemy import select


class TestDB():
    def __enter__(self):
        recreate_tables()
        return self

    def test_one(self):
        engine = get_engine()
        alice = User(username="Alice",
                     hashed_password="sdfdsfds")
        with Session(engine) as session:
            stmt = session.scalars(
                    select(User).where(User.username == "Alice")).one_or_none()
            if stmt:
                session.delete(stmt)
            try:
                session.commit()
            except Exception:
                session.rollback()
            session.add(alice)
            try:
                session.commit()
            except Exception:
                session.rollback()
            added_alice = str(session.scalars(select(User)).one())
            session.commit()
            self.assert_eq(added_alice,
                           alice.__repr__())
