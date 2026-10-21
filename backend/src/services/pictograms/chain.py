import asyncio
import re

import httpx

from src.config import settings

from .arasaac import ArasaacProvider
from .base import PictogramMatch
from .mulberry import MulberryProvider
from .openmoji import OpenMojiProvider
from .own import OwnProvider

ATTRIBUTIONS = {
    "own": "",
    "mulberry": MulberryProvider.attribution,
    "openmoji": OpenMojiProvider.attribution,
    "arasaac": ArasaacProvider.attribution,
}
ATTRIBUTION = ArasaacProvider.attribution
STOPWORDS = frozenset(
    """
    a al algo algunas algunos ante antes como con contra cual cuando de del desde donde durante
    e el ella ellas ellos en entre era eran es esa esas ese eso esos esta estaba estaban estas
    este esto estos fue fueron ha hasta hay la las le les lo los más me mi mis mucha muchas
    mucho muchos muy nada ni no nos o otra otras otro otros para pero poco por porque que quien
    se sin sobre su sus también te tener tiene tienen todo todos tu tus un una unas uno unos y ya
    """.split()
)
TOKEN_PATTERN = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")
VERB_ENDINGS = ("ar", "er", "ir", "ando", "iendo", "ado", "ido", "ó", "aron", "aba")
NOUN_ENDINGS = ("ción", "sión", "dad", "tad", "miento", "mente", "ía", "ero", "era")


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


def provider_names() -> list[str]:
    return [
        name.strip().lower()
        for name in settings.pictogram_providers.split(",")
        if name.strip().lower() in ATTRIBUTIONS
    ]


async def _match_words(
    sentences: list[str], names: list[str], client: httpx.AsyncClient | None = None
) -> tuple[list[list[dict]], list[str]]:
    providers: list[object] = []
    semaphore = asyncio.Semaphore(8) if client else None
    for name in names:
        if name == "own":
            providers.append(OwnProvider())
        elif name == "mulberry":
            providers.append(MulberryProvider())
        elif name == "openmoji":
            providers.append(OpenMojiProvider())
        elif name == "arasaac" and client and semaphore:
            providers.append(ArasaacProvider(client, semaphore))

    words_by_sentence = [select_content_words(sentence) for sentence in sentences]
    unique_words = list(dict.fromkeys(word for words in words_by_sentence for word in words))
    found: dict[str, PictogramMatch | None] = {}
    for word in unique_words:
        found[word] = None
        for provider in providers:
            match = await provider.lookup(word)
            if match is not None:
                found[word] = match
                break

    groups = [
        [found[word].as_dict() for word in words if found[word] is not None]
        for words in words_by_sentence
    ]
    used = {match["source"] for group in groups for match in group}
    attributions = [ATTRIBUTIONS[name] for name in names if name in used and ATTRIBUTIONS[name]]
    return groups, attributions


async def _lookup_sentences(sentences: list[str]) -> tuple[list[list[dict]], list[str]]:
    names = provider_names()
    if "arasaac" not in names:
        return await _match_words(sentences, names)
    timeout = httpx.Timeout(3.5, connect=2.0)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        return await _match_words(sentences, names, client)


async def pictograms_with_attributions(
    sentences: list[str], enabled: bool
) -> tuple[list[list[dict]], list[str]]:
    if not enabled:
        return [[] for _ in sentences], []
    return await _lookup_sentences(sentences)


async def pictograms_for_sentences(sentences: list[str], enabled: bool) -> list[list[dict]]:
    groups, _ = await pictograms_with_attributions(sentences, enabled)
    return groups


def clear_cache() -> None:
    from .arasaac import clear_cache as clear_arasaac_cache

    clear_arasaac_cache()
