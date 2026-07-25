from fastapi import APIRouter

from app.api.v1 import admin, bundesliga, f1, health, nfl

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(bundesliga.router, tags=["Bundesliga"])
api_router.include_router(f1.router, tags=["F1"])
api_router.include_router(nfl.router, tags=["NFL"])
api_router.include_router(admin.router, tags=["Admin"])
