from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class CreationDateMixin:
    creation_date: Mapped[datetime] = mapped_column(server_default=func.now())


class IsActiveMixin:
    is_active: Mapped[bool] = mapped_column(default=True)
