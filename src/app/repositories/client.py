from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.database.models.client import Client
from ..utils.repository import SQLAlchemyRepository


class ClientRepository(SQLAlchemyRepository):
    model = Client

    async def get_research_data(self, client_id):  #
        stmt = select(self.model).where(self.model.id == client_id).options(
            selectinload(self.model.researches))
        res = (await self.session.execute(stmt)).scalar_one()
        return res

