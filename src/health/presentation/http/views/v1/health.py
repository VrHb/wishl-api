from fastapi import APIRouter
from starlette.responses import Response

from src.session import HealthControllerDep

health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("/read", include_in_schema=False)
async def health_check(health_controlller: HealthControllerDep) -> Response:
    """Liveness probe with DB read check."""
    await health_controlller.check_read()
    return Response(status_code=200)


@health_router.get("/write", include_in_schema=False)
async def health_write_probe(health_controlller: HealthControllerDep) -> Response:
    """Readiness probe for DB write access.

    Creates a temporary table inside a short transaction and inserts a row.
    No persistent changes are made (ON COMMIT DROP).
    """
    await health_controlller.check_write()
    return Response(status_code=200)
