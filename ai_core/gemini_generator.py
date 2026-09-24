from __future__ import annotations

import os
from typing import Any

from legalease import build_template_document

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None


class GeminiDocumentGenerator:
    def generate_document(self, payload: Any) -> str:
        data = payload if isinstance(payload, dict) else payload.model_dump() if hasattr(payload, "model_dump") else payload.dict() if hasattr(payload, "dict") else {}

        if genai is not None:
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    prompt = (
                        "Draft a polished professional legal document in clear English. "
                        "Keep it practical, structured, and readable. "
                        "Return only the final document text without markdown fences. "
                        f"Document type: {data.get('document_type', 'Service Agreement')}. "
                        f"Party 1: {data.get('party_name', 'Acme Corp')}. "
                        f"Party 2: {data.get('other_party_name', 'Beta LLC')}. "
                        f"Role: {data.get('role', 'Business professional')}. "
                        f"Jurisdiction: {data.get('jurisdiction', 'Delaware, USA')}. "
                        f"Effective date: {data.get('effective_date', '2026-10-01')}. "
                        f"Deliverables: {data.get('deliverables', 'services and support')}. "
                        f"Purpose: {data.get('purpose', 'commercial cooperation')}. "
                        f"Additional terms: {data.get('additional_terms', 'confidentiality, governing law, and good-faith performance')}."
                    )
                    response = model.generate_content(prompt)
                    text = getattr(response, "text", None) or str(response)
                    if text and text.strip():
                        return text.strip()
                except Exception:
                    pass
        return build_template_document(data)
