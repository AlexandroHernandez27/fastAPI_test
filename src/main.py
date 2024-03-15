from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import (
    api_v1_router,
    healthcheck_router,
)

from core.settings import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    redirect_slashes=False,
)



# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcheck_router)
app.include_router(api_v1_router)




