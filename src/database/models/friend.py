from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from src.database.database_metadata import Base


class Friend(Base):
    __tablename__ = "frineds"

    id: Mapped[int] = mapped_column(primary_key=True)

    login: Mapped[str] = mapped_column(nullable=True)
    steam_id: Mapped[str]
    is_folowing: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


    user: Mapped["User"] = relationship(back_populates="friends")
