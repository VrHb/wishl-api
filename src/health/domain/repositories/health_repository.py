from abc import ABC, abstractmethod


class HealthRepository(ABC):
    @abstractmethod
    async def check_read(self) -> None:
        pass

    @abstractmethod
    async def check_write(self) -> None:
        pass
