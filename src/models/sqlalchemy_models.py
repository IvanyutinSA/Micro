from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column,
                            relationship)
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str]
    hashed_password: Mapped[str]
    bio: Mapped[str] = mapped_column(nullable=True)
    image_url: Mapped[str] = mapped_column(nullable=True)

    articles: Mapped[list["ArticleOwnership"]] = relationship(
            back_populates="user")
    comments: Mapped[list["CommentOwnership"]] = relationship(
            back_populates="author")

    def __repr__(self):
        return (f"({self.username}, {self.hashed_password}" +
                f" {self.bio}, {self.image_url})")


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(unique=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)

    author: Mapped["ArticleOwnership"] = relationship(
            back_populates="article")
    tag_list: Mapped[list["TagOwnership"]] = relationship(
            back_populates="article")
    comments: Mapped[list["CommentOwnership"]] = relationship(
            back_populates="article")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(unique=True)

    articles: Mapped[list["TagOwnership"]] = relationship(
            back_populates="tag")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    body: Mapped[str] = mapped_column(nullable=False)

    ownerships: Mapped[list["CommentOwnership"]] = relationship(
            back_populates="comment")


class ArticleOwnership(Base):
    __tablename__ = "article_ownership"

    user_id: Mapped[int] = mapped_column(
            ForeignKey("users.id",
                       ondelete="CASCADE"),
            primary_key=True)

    article_id: Mapped[int] = mapped_column(
            ForeignKey("articles.id",
                       ondelete="CASCADE"),
            primary_key=True)

    user: Mapped["User"] = relationship(
            back_populates="articles")
    article: Mapped["Article"] = relationship(
            back_populates="author")


class TagOwnership(Base):
    __tablename__ = "tag_ownership"

    article_id: Mapped[int] = mapped_column(
            ForeignKey("articles.id",
                       ondelete="CASCADE"),
            primary_key=True)

    tag_id: Mapped[int] = mapped_column(
            ForeignKey("tags.id",
                       ondelete="CASCADE"),
            primary_key=True)

    article: Mapped["Article"] = relationship(
            back_populates="tag_list")

    tag: Mapped["Tag"] = relationship(
            back_populates="articles")


class CommentOwnership(Base):
    __tablename__ = "comment_ownership"

    user_id: Mapped[int] = mapped_column(
            ForeignKey("users.id",
                       ondelete="CASCADE"),
            primary_key=True)

    article_id: Mapped[int] = mapped_column(
            ForeignKey("articles.id",
                       ondelete="CASCADE"),
            primary_key=True)

    comment_id: Mapped[int] = mapped_column(
            ForeignKey("comments.id",
                       ondelete="CASCADE"),
            primary_key=True)

    author: Mapped["User"] = relationship(
            back_populates="comments")

    article: Mapped["Article"] = relationship(
            back_populates="comments")

    comment: Mapped["Comment"] = relationship(
            back_populates="ownerships")
