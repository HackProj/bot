from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from src.database.database_metadata import Base


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)

    steam_id: Mapped[str] = ForeignKey("friends.id", ondelete="CASCADE")
    app_id: Mapped[str]
    app_name: Mapped[str]
    time_played: Mapped[int]

    user: Mapped["User"] = relationship(back_populates="friends")
