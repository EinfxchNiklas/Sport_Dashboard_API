from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.logging_config import configure_logging
from app.api.v1.router import api_router
from app.schedulers.scheduler import start_scheduler, shutdown_scheduler

configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.enable_scheduler:
        start_scheduler()
    yield
    if settings.enable_scheduler:
        shutdown_scheduler()


app = FastAPI(
    title="Sport Dashboard API",
    version="0.1.0",
    description="Zentrale REST-API für Sportdaten (Bundesliga, F1, NFL).",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")
