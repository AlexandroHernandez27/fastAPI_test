from fastapi import APIRouter

from api.healthcheck.endpoints import router as healthcheck_endpoints
from core.settings import settings

healthcheck_router = APIRouter()
healthcheck_router.include_router(healthcheck_endpoints)

api_v1_router = APIRouter(prefix=f"/{settings.API_V1}")
