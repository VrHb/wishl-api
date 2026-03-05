import logging

from src.health.domain.repositories.health_repository import HealthRepository

logger = logging.getLogger(__name__)


class HealthController:
    def __init__(
        self,
        health_repository: HealthRepository,
    ) -> None:
        self.health_repository = health_repository

    async def check_read(
        self,
    ) -> None:
        await self.health_repository.check_read()

    async def check_write(
        self,
    ) -> None:
        await self.health_repository.check_write()
