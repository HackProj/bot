import hashlib

from ..api.v1.utils import generate_password, generate_login
from ..schemas.client import ClientFullData, CreateClientRequest
from ..utils.unitofwork import IUnitOfWork, UnitOfWork


class ClientService:

    @classmethod
    async def create(cls,
                     model: CreateClientRequest,
                     uow: IUnitOfWork = UnitOfWork()
                     ) -> ClientFullData:
        async with uow:
            client = await uow.client.get_by_login(model.login)
            if client:
                return client.get_schema()
            res = await uow.client.add_one(data={**model.model_dump()})

            await uow.commit()
            return res
