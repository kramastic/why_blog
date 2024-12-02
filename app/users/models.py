from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    nickname: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)
    second_name: Mapped[str] = mapped_column(nullable=False)
    birthday_date: Mapped[date] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=True)
    introduction: Mapped[str] = mapped_column(String(500), nullable=True)
    avatar_id: Mapped[str] = mapped_column(nullable=True)

    articles = relationship("Articles", back_populates="user")

    def __str__(self):
        return f"User #{self.id} {self.email}"


from app.articles.models import Articles
