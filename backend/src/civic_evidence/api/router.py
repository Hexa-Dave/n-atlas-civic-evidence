# Aggregates all versioned routers under the /api prefix.
from fastapi import APIRouter

from civic_evidence.api.v1 import (
    audio,
    cases,
    civic_guidance,
    claims,
    health,
    reports,
    reviews,
    transcripts,
)

api_router = APIRouter()

for module in (health, cases, audio, transcripts, claims, reviews, civic_guidance, reports):
    api_router.include_router(module.router)
