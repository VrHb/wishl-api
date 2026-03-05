from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.exceptions import connect_all_exceptions_to_handler
from src.health.presentation.http.views.v1.health import health_router
from src.logging import app_logger
from src.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Configure logging on application startup and cleanup on shutdown."""
    # код до запуска приложения
    # можно добавить дополнительное логирование и клиенты для внешних сервисов
    # например sentry
    yield
    # код после запуска приложения


def assemble_app() -> FastAPI:
    application = FastAPI(
        title="Wishl API",
        description="API endpoints for wishlists service",
        root_path=settings.API_PREFIX,
        lifespan=lifespan,
        version="0.1.0",
    )

    application.include_router(health_router)

    application.logger = app_logger

    connect_all_exceptions_to_handler(application)

    return application


app = assemble_app()
