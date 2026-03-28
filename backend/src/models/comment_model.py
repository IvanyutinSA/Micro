import inspect

from src.schemas import (Comment as CommentSchema,
                         FullComment)
from src.models.sqlalchemy_models import (Comment,
                                          CommentOwnership,
                                          Article)
from src.models.sqlalchemy_db import get_engine

from src.models.article_model import ArticleModel
from sqlalchemy.orm import Session
from sqlalchemy import select


def force_session(f, arg_name="session", engine=None):
    engine = engine if engine else get_engine()

    def wrapper(*args, **kwargs):
        sig = inspect.signature(f)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        if arg_name in bound.arguments:
            return f(*args, **kwargs)

        with Session(engine) as session:
            try:
                kwargs[arg_name] = session
                result = f(*args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                raise e

    return wrapper


class CommentModel:
    def __init__(self):
        self.article_model = ArticleModel()

    def __create_naked(self, comment: Comment, session: Session):
        session.add(comment)
        session.flush()

    def __build_relation(self,
                         user_id: int,
                         article_id: int,
                         comment_id: int,
                         session: Session):
        own = CommentOwnership(user_id=user_id,
                               article_id=article_id,
                               comment_id=comment_id)
        session.add(own)

    @force_session
    def is_owned_by_user(self,
                         user_id: int,
                         comment_id: int,
                         session: Session) -> bool:
        own = session.scalars(
                select(CommentOwnership)
                .where((CommentOwnership.user_id == user_id) &
                       (CommentOwnership.comment_id == comment_id))
                ).one_or_none()
        return own is not None

    @force_session
    def create(self,
               request: Comment,
               slug: str,
               user_id: int,
               session: Session) -> bool:
        article = self.article_model.get_full(slug, session)
        if article is None:
            return False
        comment = Comment(body=request.body)
        self.__create_naked(comment, session)
        self.__build_relation(user_id, article.id,
                              comment.id, session)
        return True

    @force_session
    def get(self, slug: str, session: Session) -> list[FullComment]:
        article = self.article_model.get_full(slug, session)
        if article is None:
            return []
        owns = [FullComment(id=own.comment.id,
                            body=own.comment.body)
                for own in article.comments]
        return owns

    @force_session
    def delete(self,
               comment_id: int,
               session: Session) -> int:
        return session.query(Comment).filter_by(id=comment_id).delete()
