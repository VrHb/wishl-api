from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.health.domain.repositories.health_repository import HealthRepository


class HealthDatabaseRepository(HealthRepository):
    """Infrastructure repository for health/readiness DB probes."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def check_read(self) -> None:
        await self._db.execute(text("SELECT 1"))

    async def check_write(self) -> None:
        async with self._db.begin():
            await self._db.execute(text("CREATE TEMP TABLE IF NOT EXISTS healthcheck_write(i int) ON COMMIT DROP"))
            await self._db.execute(text("INSERT INTO healthcheck_write(i) VALUES (1)"))
