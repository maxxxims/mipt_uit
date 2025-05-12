from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
from datetime import datetime


class FeedBack(Base):
    __tablename__ = "feedback"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    tg_id: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(default=datetime.now)
    email: Mapped[str] = mapped_column(nullable=True)
    is_sent: Mapped[bool] = mapped_column(default=False)