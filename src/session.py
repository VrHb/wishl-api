from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.health.data.repositories.database.health_database_repository import HealthDatabaseRepository
from src.health.domain.controllers.health import HealthController
from src.health.domain.repositories.health_repository import HealthRepository
from src.settings import settings

engine = create_async_engine(settings.create_database_url, echo=False, future=True, pool_pre_ping=True)

SessionFactory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with SessionFactory() as db:
        yield db


def health_repository_factory(db: Annotated[AsyncSession, Depends(get_db)]) -> HealthRepository:
    return HealthDatabaseRepository(db=db)


HealthRepositoryDep = Annotated[HealthRepository, Depends(health_repository_factory)]


def health_controller_factory(health_repository: HealthRepositoryDep) -> HealthController:
    return HealthController(health_repository=health_repository)


HealthControllerDep = Annotated[HealthController, Depends(health_controller_factory)]
