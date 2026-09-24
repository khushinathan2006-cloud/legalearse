from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from routes import router

APP_NAME = "LegalEase"

app = FastAPI(
    title=APP_NAME,
    description="AI-powered legal document generation backend",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to LegalEase API"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": APP_NAME}
