from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db import Base
from uuid import uuid4, UUID
from datetime import datetime


class Request(Base):
    __tablename__ = "requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(default=datetime.now)
