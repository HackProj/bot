from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from src.database.models.mixin import IsActiveMixin, CreationDateMixin
from src.database.database_metadata import Base
from src.app.schemas.client import ClientFullData


# Модель клиента \
class Client(Base, CreationDateMixin, IsActiveMixin):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column()

    researches: Mapped[List["Research"]] = relationship(back_populates="client")

    def get_schema(self) -> ClientFullData:
        return ClientFullData(
            id=self.id,
            login=self.login,
            creation_date=self.creation_date,
            is_active=self.is_active
        )

    #
    def __str__(self):
        return f" Клиент: {self.login}"

    def error_message(self):
        return f" Client: {self.login}   id: {self.id}"
