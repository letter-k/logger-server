from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import main
from app.core.config import settings

app = FastAPI(
    title="logger-server-api",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(main.api_router, prefix=settings.API_V1_STR)
