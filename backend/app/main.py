"""
FastAPI application entry point.

This file is complete as-is. It wires up CORS, registers the routers,
and defines the application lifespan.

Database schema is managed by Alembic migrations (see alembic/).
The Dockerfile runs `alembic upgrade head` before starting the server.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import search_router
from app.routers import files_router, folders_router

from app.logger import get_logger


logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up File Explorer API")
    yield
    logger.info("Shutting down File Explorer API")


app = FastAPI(title="File Explorer API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(folders_router.router)
app.include_router(files_router.router)
app.include_router(search_router.router)


@app.get("/health", tags=["health"])
def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}