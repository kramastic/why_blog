from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey, func




class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(nullable=False)
    send_datetime: Mapped[datetime] = mapped_column(server_default=func.now())
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    recipient = relationship("Users", foreign_keys=[recipient_id])
    sender = relationship("Users", foreign_keys=[sender_id])
    
    
from app.users.models import Users
