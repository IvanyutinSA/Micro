from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models.sqlalchemy_models import (Article,
                                          Tag,
                                          ArticleOwnership,
                                          TagOwnership)
from src.models.sqlalchemy_db import get_engine

from src.schemas import (CreateArticleRequest,
                         Article as ArticleSchema,
                         CompleteArticle)

import inspect


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


class TagModel:
    def create(self, name: str, session: Session) -> bool:
        tag = Tag(tag=name)
        session.add(tag)

    def get(self, name: str, session: Session) -> Tag | None:
        tag: Tag = session.scalars(select(Tag)
                                   .where(Tag.tag == name)
                                   ).one_or_none()
        return tag

    def get_or_create(self, name: str, session: Session) -> Tag:
        tag = self.get(name, session)
        if tag is None:
            self.create(name, session)
            tag = self.get(name, session)
        return tag


class ArticleModel:
    def __init__(self):
        self.tag_model = TagModel()

    def __create_naked(self, article: Article, session: Session):
        session.add(article)

    def __build_relation_tag(self, article_id: int,
                             tag_id: int, session: Session):
        ownership = TagOwnership(article_id=article_id,
                                 tag_id=tag_id)
        session.add(ownership)

    def __drop_relation_tag(self, article_id: int,
                            tag_id: int, session: Session):
        result = session.query(TagOwnership).filter_by(
                article_id=article_id,
                tag_id=tag_id).delete()
        return result

    def __build_relation_user(self, user_id: int, article_id: int,
                              session: Session):
        ownership = ArticleOwnership(user_id=user_id,
                                     article_id=article_id)
        session.add(ownership)

    def get_full(self, slug: str, session: Session) -> Article:
        article: Article = session.scalars(select(Article)
                                           .where(Article.slug == slug)
                                           ).one_or_none()
        return article

    @force_session
    def get_complete(self, slug: str, session: Session):
        article = self.get_full(slug, session)
        tag_list = [tag.tag.tag for tag in article.tag_list]
        response = CompleteArticle(id=article.id,
                                   slug=article.slug,
                                   title=article.title,
                                   description=article.description,
                                   body=article.body,
                                   tag_list=tag_list)
        return response

    @force_session
    def get_all(self, session: Session) -> list[ArticleSchema]:
        articles = session.scalars(select(Article)).all()
        articles_schema = []
        for article in articles:
            tag_list = [tag.tag.tag for tag in article.tag_list]
            article_schema = ArticleSchema(title=article.title,
                                           description=article.description,
                                           body=article.body,
                                           tag_list=tag_list)
            articles_schema.append(article_schema)
        return articles_schema

    @force_session
    def is_user_own_article_by_slug(self,
                                    user_id: int,
                                    slug: str,
                                    session: Session) -> bool:
        article = session.scalars(select(Article)
                                  .where(Article.slug == slug)
                                  ).one_or_none()
        if article is None:
            return False
        article_id = article.id
        owns = session.scalars(select(ArticleOwnership)
                               .where(ArticleOwnership.user_id == user_id)
                               ).all()
        for own in owns:
            if own.article_id == article_id:
                return True
        return False

    @force_session
    def create(self, request: CreateArticleRequest,
               session: Session) -> bool:
        user_id = request.user_id
        slug = request.slug
        tag_list = request.tag_list
        article = Article(slug=slug,
                          title=request.title,
                          description=request.description,
                          body=request.body)
        self.__create_naked(article, session)
        article: Article = self.get_full(slug, session)
        self.__build_relation_user(user_id, article.id, session)
        for tag_name in tag_list:
            tag = self.tag_model.get_or_create(tag_name, session)
            self.__build_relation_tag(article.id, tag.id, session)
        return True

    @force_session
    def get(self, slug: str, session: Session) -> ArticleSchema | None:
        article: Article = session.scalars(select(Article)
                                           .where(Article.slug == slug)
                                           ).one_or_none()
        if article is None:
            return None
        tag_list = [tag.tag.tag for tag in article.tag_list]
        response = ArticleSchema(title=article.title,
                                 description=article.description,
                                 body=article.body,
                                 tag_list=tag_list)
        return response

    @force_session
    def update(self, request: ArticleSchema, slug: str, session: Session):
        article = self.get_full(slug, session)

        article.title = request.title
        article.description = request.description
        article.body = request.body

        old_tag_list = [tag.tag.tag for tag in article.tag_list]

        for tag_name in set(request.tag_list):
            if tag_name in old_tag_list:
                continue
            tag = self.tag_model.get_or_create(tag_name, session)
            self.__build_relation_tag(article.id, tag.id, session)

        for tag_own in article.tag_list:
            if tag_own.tag.tag in request.tag_list:
                continue
            self.__drop_relation_tag(article.id, tag_own.tag.id, session)

    @force_session
    def delete(self, slug: str, session: Session) -> int:
        return session.query(Article).filter_by(slug=slug).delete()
