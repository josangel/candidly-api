from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints import analyze, ping
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Candidly API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.include_router(ping.router, prefix="/api/v1")
app.include_router(analyze.router, prefix="/api/v1")
