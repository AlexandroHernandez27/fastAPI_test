from fastapi import APIRouter, status

from api.healthcheck.schemas import HealthCheckSchema
from core.settings import settings
from core.utils.responses import EnvelopeResponse, EnvelopeResponseBody

router = APIRouter(tags=["Health Check"])


@router.get(
    "/health-check", status_code=status.HTTP_200_OK, summary="Health check service", response_model=EnvelopeResponse
)
def health_check() -> EnvelopeResponse:
    result = HealthCheckSchema(detail=settings.PROJECT_NAME, version=settings.VERSION)

    body = EnvelopeResponseBody(links=None, count=None, results=result)
    return EnvelopeResponse(errors=None, body=body)
