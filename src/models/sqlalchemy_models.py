from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True, unique=True)
    hashed_password: Mapped[str]
    bio: Mapped[str] = mapped_column(nullable=True)
    image_url: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return f"({self.username}, {self.hashed_password}, {self.bio}, {self.image_url})"
