from collections import OrderedDict
from contextlib import asynccontextmanager
from re import compile
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool

from src.database.config import DBSettings


class DatabaseAccessor:
    _db_settings = None
    DEFAULT_ACQUIRE_TIMEOUT: float = 1
    DEFAULT_REFRESH_DELAY: float = 1
    DEFAULT_REFRESH_TIMEOUT: float = 5
    DEFAULT_MASTER_AS_REPLICA_WEIGHT: float = 0.0
    DEFAULT_STOPWATCH_WINDOW_SIZE: int = 128
    SEARCH_HOST_REGEXP = compile(r'host=(.+?)\s')

    def __init__(self, db_settings: DBSettings, statement_cache_size: int = 0):
        print(id(self), "Вызвали конструктор создания дб ацессора")
        self._db_settings = db_settings
        self._dsn = self._db_settings.get_dsn_async()
        self._session_makers = OrderedDict()
        self._statement_cache_size = statement_cache_size
        self._async_session_maker = None

    async def run(self) -> None:
        await self._set_engine()

    async def _set_engine(self) -> None:
        self.engine = create_async_engine(
            self._dsn,
            pool_pre_ping=True,
            poolclass=NullPool,
            future=True,
            echo=False,
        )

    def new_run(self) -> None:
        self._set_engine_sync()

    def _set_engine_sync(self) -> None:
        self.engine = create_async_engine(
            self._dsn,
            pool_pre_ping=True,
            poolclass=NullPool,
            future=True,
            echo=False,
        )

    async def init_db(self, Base) -> None:
        """use it if u not use alembic """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    def _create_session(self) -> None:
        self._async_session_maker = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)

    def get_sync_session(self):
        return scoped_session(sessionmaker(bind=self.engine, expire_on_commit=False, ))

    def get_async_session_maker(self) -> sessionmaker:
        return sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        self._create_session()
        async with self._async_session_maker() as session:
            yield session

    async def stop(self) -> None:
        await self.engine.dispose()
