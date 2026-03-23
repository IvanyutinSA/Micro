from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, DateTime, UniqueConstraint
from datetime import datetime


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
    subscription_key: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return (f"({self.username}, {self.hashed_password}" +
                f" {self.bio}, {self.image_url})")


class Subscribers(Base):
    __tablename__ = "subscribers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subscriber_id: Mapped[int]
    author_id: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (UniqueConstraint("subscriber_id",
                                       "author_id",
                                       name="ux_sub_unique"),)
