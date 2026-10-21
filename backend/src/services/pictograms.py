import asyncio
import logging
import re
import time
from urllib.parse import quote

import httpx

logger = logging.getLogger(__name__)

ARASAAC_API = "https://api.arasaac.org/v1/pictograms/es/search"
ARASAAC_IMAGE = "https://static.arasaac.org/pictograms/{id}/{id}_300.png"
ATTRIBUTION = (
    "Pictogramas: Sergio Palao. Origen: ARASAAC (http://www.arasaac.org). "
    "Licencia: CC (BY-NC-SA). Propiedad: Gobierno de Aragón (España)"
)
CACHE_TTL_SECONDS = 900
STOPWORDS = frozenset(
    """
    a al algo algunas algunos ante antes como con contra cual cuando de del desde donde durante
    e el ella ellas ellos en entre era eran es esa esas ese eso esos esta estaba estaban estas
    este esto estos fue fueron ha hasta hay la las le les lo los más me mi mis mucha muchas
    mucho muchos muy nada ni no nos o otra otras otro otros para pero poco por porque que quien
    se sin sobre su sus también te tener tiene tienen todo todos tu tus un una unas uno unos y
    ya
    """.split()
)
TOKEN_PATTERN = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")
VERB_ENDINGS = ("ar", "er", "ir", "ando", "iendo", "ado", "ido", "ó", "aron", "aba")
NOUN_ENDINGS = ("ción", "sión", "dad", "tad", "miento", "mente", "ía", "ero", "era")

_cache: dict[str, tuple[float, int | None]] = {}


def clear_cache() -> None:
    _cache.clear()


def select_content_words(sentence: str, limit: int = 3) -> list[str]:
    words = TOKEN_PATTERN.findall(sentence.lower())
    candidates = [
        (index, word)
        for index, word in enumerate(words)
        if word not in STOPWORDS and len(word) >= 3
    ]

    def priority(item: tuple[int, str]) -> tuple[int, int]:
        index, word = item
        if word.endswith(VERB_ENDINGS):
            group = 0
        elif word.endswith(NOUN_ENDINGS):
            group = 1
        else:
            group = 2
        return group, index

    selected = sorted(candidates, key=priority)[:limit]
    return [word for _, word in selected]


async def _lookup_id(
    client: httpx.AsyncClient,
    keyword: str,
    semaphore: asyncio.Semaphore,
) -> int | None:
    normalized = keyword.lower()
    cached = _cache.get(normalized)
    if cached and cached[0] > time.monotonic():
        return cached[1]

    async with semaphore:
        try:
            response = await client.get(f"{ARASAAC_API}/{quote(normalized)}")
            response.raise_for_status()
            data = response.json()
            arasaac_id = data[0].get("_id") if isinstance(data, list) and data else None
            if isinstance(arasaac_id, int):
                _cache[normalized] = (time.monotonic() + CACHE_TTL_SECONDS, arasaac_id)
                return arasaac_id
            _cache[normalized] = (time.monotonic() + CACHE_TTL_SECONDS, None)
            return None
        except (httpx.HTTPError, ValueError, TypeError):
            logger.info("ARASAAC lookup unavailable for %s", normalized)
            return None


async def pictograms_for_sentences(
    sentences: list[str],
    enabled: bool,
) -> list[list[dict[str, str | int]]]:
    if not enabled:
        return [[] for _ in sentences]

    words_by_sentence = [select_content_words(sentence) for sentence in sentences]
    unique_words = list(dict.fromkeys(word for words in words_by_sentence for word in words))
    if not unique_words:
        return [[] for _ in sentences]

    timeout = httpx.Timeout(3.5, connect=2.0)
    semaphore = asyncio.Semaphore(8)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        ids = await asyncio.gather(*(_lookup_id(client, word, semaphore) for word in unique_words))

    lookup = dict(zip(unique_words, ids, strict=True))
    return [
        [
            {
                "keyword": word,
                "arasaac_id": arasaac_id,
                "image_url": ARASAAC_IMAGE.format(id=arasaac_id),
            }
            for word in words
            if (arasaac_id := lookup.get(word)) is not None
        ]
        for words in words_by_sentence
    ]
