from src.models.sqlalchemy_models import Subscribers

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models.sqlalchemy_db import get_engine

from src.schemas import Subscribers as SubscribersSchema


class SubscribersModel:
    def __init__(self, engine=None):
        self.engine = engine if engine else get_engine()

    def create(self, sub_id: int, auth_id: int):
        with Session(self.engine) as session:
            sub = Subscribers(subscriber_id=sub_id,
                              author_id=auth_id)
            session.add(sub)
            session.commit()

    def get_by_auth_id(self, auth_id: int) -> SubscribersSchema:
        with Session(self.engine) as session:
            subs = session.scalars(select(Subscribers)
                                   .where(Subscribers.author_id == auth_id)
                                   ).all()
            ids = [sub.subscriber_id for sub in subs]
            reply = SubscribersSchema(sub_ids=ids)
            return reply
