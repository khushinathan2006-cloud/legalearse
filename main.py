from fastapi import FastAPI

from routes import router

app = FastAPI(
    title="LegalEase API",
    description="AI-powered legal document generation backend",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to LegalEase API"}
