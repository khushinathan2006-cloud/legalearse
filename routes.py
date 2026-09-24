from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str = Field(default="Service Agreement")
    party_name: str = Field(default="Acme Corp")
    other_party_name: str = Field(default="Beta LLC")
    jurisdiction: str = Field(default="Delaware, USA")
    effective_date: str = Field(default="2026-10-01")
    purpose: str = Field(default="commercial cooperation")
    additional_terms: str = Field(default="confidentiality, governing law, and good-faith performance")
    role: str = Field(default="Business professional")
    deliverables: str = Field(default="services and support")


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "LegalEase"}


@router.post("/generate")
async def generate_document(payload: DocumentRequest) -> dict[str, str]:
    try:
        generator = GeminiDocumentGenerator()
        document_text = generator.generate_document(payload.model_dump())
        return {"document": document_text}
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Generation failed: {exc}") from exc
