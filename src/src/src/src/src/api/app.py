from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from src.extractor import extract_entities_from_text

app = FastAPI(
    title="Financial News Entity Extraction API",
    description="Gen AI-based extraction of financial entities from news text",
    version="0.1.0",
)


class NewsRequest(BaseModel):
    text: str
    model: str | None = "gpt-4.1-mini"


class EntitiesResponse(BaseModel):
    entities: Dict[str, list]


@app.post("/extract", response_model=EntitiesResponse)
async def extract_entities(payload: NewsRequest):
    entities = extract_entities_from_text(payload.text, model=payload.model)
    return {"entities": entities}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
