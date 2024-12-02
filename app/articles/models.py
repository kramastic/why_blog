from datetime import datetime

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Articles(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_link: Mapped[str] = mapped_column(nullable=True)
    create_datetime: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    image_id: Mapped[str] = mapped_column(nullable=True)

    user = relationship("Users", back_populates="articles")

    def __str__(self):
        return f"Article #{self. id}"


from app.users.models import Users
