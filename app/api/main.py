from fastapi import APIRouter

from app.api.routes import logger, login, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(logger.router, prefix="/logger", tags=["logger"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
