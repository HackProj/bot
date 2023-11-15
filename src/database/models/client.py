from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from src.database.database_metadata import Base
from src.bot.schemas.client import ClientFullData


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column()

    researches: Mapped[List["Research"]] = relationship(back_populates="client")

    def get_schema(self) -> ClientFullData:
        return ClientFullData(
            id=self.id,
            login=self.login,
        )

    #
    def __str__(self):
        return f" Клиент: {self.login}"

    def error_message(self):
        return f" Client: {self.login}   id: {self.id}"
