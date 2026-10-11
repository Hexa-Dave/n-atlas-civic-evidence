# FastAPI application entry point for the Civic Evidence backend.
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from civic_evidence.api.router import api_router
from civic_evidence.config import get_settings
from civic_evidence.dependencies import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_settings()  # fail fast when configuration is invalid
    initialize_database()
    yield


settings = get_settings()

app = FastAPI(title="N-ATLAS Civic Evidence API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
