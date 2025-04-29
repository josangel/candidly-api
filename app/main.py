"""Module to create the FastAPI application instance and include routers."""

from fastapi import FastAPI

from app.api.v1.endpoints import analyze, ping
from core.config import settings
from services.assembly.mock import MockAssemblyService
from services.assembly.prod import AssemblyService

if settings.assembly_mock:
    ia_service = MockAssemblyService()
else:
    ia_service = AssemblyService()


app = FastAPI()

app.include_router(ping.router, prefix="/api/v1")
app.include_router(analyze.router, prefix="/api/v1")
