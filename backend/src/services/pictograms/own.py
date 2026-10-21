import json
from pathlib import Path
from urllib.parse import quote

from src.config import settings

from .base import PictogramMatch
from .normalization import lookup_forms, normalize_word

ASSET_DIR = Path(__file__).resolve().parents[3] / "assets" / "pictograms" / "own"
INDEX_PATH = ASSET_DIR / "index.json"


def _load_index() -> dict[str, dict[str, str]]:
    entries = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    result: dict[str, dict[str, str]] = {}
    for entry in entries:
        for keyword in entry["keywords"]:
            result[normalize_word(keyword)] = entry
    return result


INDEX = _load_index()


class OwnProvider:
    source = "own"
    attribution = ""

    async def lookup(self, keyword: str) -> PictogramMatch | None:
        entry = next((INDEX[form] for form in lookup_forms(keyword) if form in INDEX), None)
        if entry is None:
            return None
        base_url = settings.public_base_url.rstrip("/")
        return PictogramMatch(
            source=self.source,
            keyword=keyword,
            pictogram_id=entry["id"],
            image_url=f"{base_url}/pictograms/own/{quote(entry['file'])}",
            license="proprietary",
            commercial_use=True,
        )
