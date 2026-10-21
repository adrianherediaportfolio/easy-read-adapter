from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from pypdf import PdfReader

from src.config import settings
from src.database import delete_adaptation, get_adaptation, list_adaptations, save_adaptation
from src.models import (
    AdaptationLevel,
    AdaptationRequest,
    AdaptationResponse,
    AdaptationSummary,
    AdaptedSentence,
    Pictogram,
    ReadabilityResult,
    ReadabilityScore,
)
from src.services.adaptation import adapt_text
from src.services.pictograms import ATTRIBUTION, pictograms_for_sentences
from src.services.readability import calculate_readability

router = APIRouter(prefix="/api", tags=["adaptations"])
MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_TEXT_CHARS = 20_000


async def _create_adaptation(
    text: str,
    level: AdaptationLevel,
    pictograms: bool,
    source: str | None,
) -> AdaptationResponse:
    adapted_text, engine = await adapt_text(text, level)
    sentence_texts = [line.strip() for line in adapted_text.splitlines() if line.strip()]
    pictogram_groups = await pictograms_for_sentences(sentence_texts, pictograms)
    sentences = [
        AdaptedSentence(
            text=sentence,
            pictograms=[Pictogram(**pictogram) for pictogram in group],
        )
        for sentence, group in zip(sentence_texts, pictogram_groups, strict=True)
    ]
    response = AdaptationResponse(
        id=str(uuid4()),
        created_at=datetime.now(UTC).isoformat(),
        level=level,
        source=source,
        original_text=text,
        adapted_text=adapted_text,
        sentences=sentences,
        readability=ReadabilityResult(
            original=ReadabilityScore(**calculate_readability(text)),
            adapted=ReadabilityScore(**calculate_readability(adapted_text)),
        ),
        engine=engine,
        attribution=ATTRIBUTION,
    )
    save_adaptation(response.model_dump(mode="json"))
    return response


@router.post(
    "/adaptations",
    response_model=AdaptationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_adaptation(request: AdaptationRequest) -> AdaptationResponse:
    return await _create_adaptation(
        request.text,
        request.level,
        request.pictograms,
        request.source,
    )


@router.post(
    "/adaptations/upload",
    response_model=AdaptationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_adaptation(
    file: UploadFile = File(...),
    level: AdaptationLevel = Form("lectura_facil"),
    pictograms: bool = Form(True),
) -> AdaptationResponse:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".txt", ".pdf"}:
        raise HTTPException(status_code=422, detail="Sube un archivo PDF o TXT.")

    content = await file.read(MAX_FILE_BYTES + 1)
    if len(content) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="El archivo supera el límite de 5 MB.")
    if not content:
        raise HTTPException(status_code=422, detail="El archivo está vacío.")

    if suffix == ".txt":
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            raise HTTPException(
                status_code=422,
                detail="El archivo TXT debe estar en UTF-8.",
            ) from error
    else:
        try:
            reader = PdfReader(BytesIO(content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        except Exception as error:
            raise HTTPException(
                status_code=422,
                detail="No se pudo leer el archivo PDF.",
            ) from error

    if not text.strip():
        raise HTTPException(status_code=422, detail="No se encontró texto en el archivo.")
    if len(text) > MAX_TEXT_CHARS:
        raise HTTPException(
            status_code=413,
            detail="El texto supera el límite de 20.000 caracteres.",
        )

    return await _create_adaptation(text, level, pictograms, None)


@router.get("/adaptations", response_model=list[AdaptationSummary])
async def get_adaptations() -> list[dict]:
    return list_adaptations()


@router.get("/adaptations/{adaptation_id}", response_model=AdaptationResponse)
async def get_adaptation_by_id(adaptation_id: str) -> dict:
    adaptation = get_adaptation(adaptation_id)
    if adaptation is None:
        raise HTTPException(status_code=404, detail="No se encontró la adaptación.")
    return adaptation


@router.delete("/adaptations/{adaptation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_adaptation(adaptation_id: str) -> None:
    if not delete_adaptation(adaptation_id):
        raise HTTPException(status_code=404, detail="No se encontró la adaptación.")
    return None


@router.get("/health")
async def health() -> dict[str, bool | str]:
    return {"status": "ok", "ai_enabled": bool(settings.openai_api_key.strip())}
