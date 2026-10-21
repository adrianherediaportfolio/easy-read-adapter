import asyncio
import logging
import time
from urllib.parse import quote

import httpx

from .base import PictogramMatch
from .normalization import lookup_forms

logger = logging.getLogger(__name__)
ARASAAC_API = "https://api.arasaac.org/v1/pictograms/es/search"
ARASAAC_IMAGE = "https://static.arasaac.org/pictograms/{id}/{id}_300.png"
CACHE_TTL_SECONDS = 900
_cache: dict[str, tuple[float, int | None]] = {}


def clear_cache() -> None:
    _cache.clear()


class ArasaacProvider:
    source = "arasaac"
    attribution = (
        "Pictogramas: Sergio Palao. Origen: ARASAAC (http://www.arasaac.org). "
        "Licencia: CC (BY-NC-SA). Propiedad: Gobierno de Aragón (España)"
    )

    def __init__(self, client: httpx.AsyncClient, semaphore: asyncio.Semaphore):
        self.client = client
        self.semaphore = semaphore

    async def lookup(self, keyword: str) -> PictogramMatch | None:
        for form in lookup_forms(keyword):
            arasaac_id = await self._lookup_id(form)
            if arasaac_id is not None:
                return PictogramMatch(
                    source=self.source,
                    keyword=keyword,
                    pictogram_id=str(arasaac_id),
                    image_url=ARASAAC_IMAGE.format(id=arasaac_id),
                    license="CC BY-NC-SA 4.0",
                    commercial_use=False,
                )
        return None

    async def _lookup_id(self, keyword: str) -> int | None:
        cached = _cache.get(keyword)
        if cached and cached[0] > time.monotonic():
            return cached[1]
        async with self.semaphore:
            try:
                response = await self.client.get(f"{ARASAAC_API}/{quote(keyword)}")
                response.raise_for_status()
                data = response.json()
                pictogram_id = data[0].get("_id") if isinstance(data, list) and data else None
                result = pictogram_id if isinstance(pictogram_id, int) else None
                _cache[keyword] = (time.monotonic() + CACHE_TTL_SECONDS, result)
                return result
            except (httpx.HTTPError, ValueError, TypeError):
                logger.info("ARASAAC lookup unavailable for %s", keyword)
                _cache[keyword] = (time.monotonic() + CACHE_TTL_SECONDS, None)
                return None
