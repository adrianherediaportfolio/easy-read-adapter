from typing import Literal

from pydantic import BaseModel, Field, field_validator

AdaptationLevel = Literal["lectura_facil", "simplificado"]


class AdaptationRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20_000)
    level: AdaptationLevel = "lectura_facil"
    pictograms: bool = True
    source: str | None = None

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El texto no puede estar vacío.")
        return value


class Pictogram(BaseModel):
    keyword: str
    arasaac_id: int
    image_url: str


class AdaptedSentence(BaseModel):
    text: str
    pictograms: list[Pictogram]


class ReadabilityScore(BaseModel):
    score: float
    label: str


class ReadabilityResult(BaseModel):
    original: ReadabilityScore
    adapted: ReadabilityScore


class AdaptationResponse(BaseModel):
    id: str
    created_at: str
    level: AdaptationLevel
    source: str | None
    original_text: str
    adapted_text: str
    sentences: list[AdaptedSentence]
    readability: ReadabilityResult
    engine: Literal["openai", "rules"]
    attribution: str


class AdaptationSummary(BaseModel):
    id: str
    created_at: str
    level: AdaptationLevel
    preview: str
