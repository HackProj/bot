from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from src.database.database_metadata import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id : Mapped[str]
    hints : Mapped[bool]

    # researches: Mapped[List["Research"]] = relationship(back_populates="client")
