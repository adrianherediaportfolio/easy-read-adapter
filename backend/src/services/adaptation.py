import logging
import re

from openai import AsyncOpenAI

from src.config import settings
from src.models import AdaptationLevel

logger = logging.getLogger(__name__)

SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+|\s*[;:]\s*")
LONG_CLAUSE_MARKER = re.compile(
    r",\s+(?:y|pero|porque|aunque|mientras|además|sin embargo)\s+"
    r"|\s+(?:pero|porque|aunque|mientras|sin embargo)\s+",
    re.IGNORECASE,
)
LONG_CLAUSE_WITH_Y = re.compile(r"\s+y\s+", re.IGNORECASE)


def _ensure_terminal_punctuation(text: str) -> str:
    if text and text[-1] not in ".!?":
        return f"{text}."
    return text


def _split_long_clause(text: str, threshold: int) -> list[str]:
    if len(text) <= threshold:
        return [text]

    match = LONG_CLAUSE_MARKER.search(text)
    if match is None:
        match = LONG_CLAUSE_WITH_Y.search(text)
    if match is None:
        return [text]

    left = text[: match.start()].strip(" ,")
    right = text[match.end() :].strip()
    if not left or not right:
        return [text]
    return [
        *_split_long_clause(_ensure_terminal_punctuation(left), threshold),
        *_split_long_clause(right, threshold),
    ]


def split_sentences(text: str, level: AdaptationLevel = "lectura_facil") -> list[str]:
    normalized = re.sub(r"[\r\n]+", " ", text).strip()
    threshold = 145 if level == "lectura_facil" else 210
    pieces = SENTENCE_BOUNDARY.split(normalized)
    sentences: list[str] = []

    for piece in pieces:
        cleaned = re.sub(r"^\s*(?:[-*•]\s*)+", "", piece).strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        if cleaned:
            sentences.extend(_split_long_clause(cleaned, threshold))

    return [sentence for sentence in sentences if sentence.strip()]


def simplify_text(text: str, level: AdaptationLevel = "lectura_facil") -> str:
    return "\n".join(split_sentences(text, level))


async def adapt_text(text: str, level: AdaptationLevel) -> tuple[str, str]:
    api_key = settings.openai_api_key.strip()
    if not api_key:
        return simplify_text(text, level), "rules"

    intensity = (
        "Aplica una adaptación estricta para Lectura Fácil."
        if level == "lectura_facil"
        else "Simplifica el texto con claridad y conserva más detalles."
    )
    prompt = (
        "Adapta el texto al español para una persona con dificultades de lectura. "
        "Escribe una idea por frase. Usa frases cortas, palabras comunes y voz activa. "
        "No uses metáforas. Explica las palabras difíciles con palabras sencillas. "
        "Pon cada frase en una línea. No añadas títulos ni información nueva. "
        f"{intensity}\n\nTexto:\n{text}"
    )

    try:
        client = AsyncOpenAI(api_key=api_key)
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "Eres especialista en Lectura Fácil en español.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content or ""
        if content.strip():
            return simplify_text(content, level), "openai"
    except Exception:
        logger.exception("OpenAI adaptation failed. Using the local rules.")

    return simplify_text(text, level), "rules"
