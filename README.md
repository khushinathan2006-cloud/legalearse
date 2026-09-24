# LegalEase

LegalEase is an AI-powered legal document generator for founders, business teams, independent contractors, and organizations that need fast drafting and export support.

## Features

- Generate professional legal drafts for service agreements, NDAs, employment agreements, and consulting agreements
- Accept party details, jurisdiction, roles, dates, scope, purpose, and custom terms
- Use Gemini AI when configured, with a structured fallback template when the API is unavailable
- Export the final draft as PDF, DOCX, or plain text
- Streamlit UI for quick editing, branding, and export flow
- FastAPI backend with `/health` and `/generate` endpoints

## Project structure

- `app.py` — Streamlit UI
- `main.py` — API entry point
- `routes.py` — request model and route handlers
- `legalease.py` — document generation and export logic
- `ai_core/gemini_generator.py` — Gemini integration fallback wrapper
- `requirements.txt` — Python dependencies

## Quick start

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Add your API key(s) to `.env`.
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
5. Run the FastAPI backend optionally:
   ```bash
   uvicorn main:app --reload
   ```

## Local API example

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "document_type": "Service Agreement",
    "party_name": "Acme Corp",
    "other_party_name": "Beta LLC",
    "jurisdiction": "Delaware, USA",
    "effective_date": "2026-10-01",
    "purpose": "software services and support",
    "additional_terms": "confidentiality, governing law, and mutual cooperation",
    "role": "Senior Product Manager",
    "deliverables": "software development and implementation support"
  }'
```

## Deployment notes

For production deployment, use a service such as Render, Railway, or a VM with:
- a Python environment
- environment variables for GEMINI_API_KEY
- a gunicorn or uvicorn process manager

## Legal note

This project is designed to assist with drafting and document export. Final legal review should always be handled by a qualified legal professional before business use.
