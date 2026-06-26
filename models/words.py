from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from models import Base

class Words(Base):
    __tablename__ = 'words'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    word: Mapped[str] = mapped_column(String(length=100))
    translate: Mapped[str] = mapped_column(String(length=100), nullable=True)
    context: Mapped[str] = mapped_column(String(length=1000), nullable=True)

