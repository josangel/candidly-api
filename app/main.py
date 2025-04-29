"""Module to create the FastAPI application instance and include routers."""

from fastapi import FastAPI

from app.api.v1.endpoints import analyze, ping

app = FastAPI()

app.include_router(ping.router, prefix="/api/v1")
app.include_router(analyze.router, prefix="/api/v1")
