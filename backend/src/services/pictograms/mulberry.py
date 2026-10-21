import json
from pathlib import Path
from urllib.parse import quote

from src.config import settings

from .base import PictogramMatch
from .normalization import lookup_forms, normalize_word

ASSET_DIR = Path(__file__).resolve().parents[3] / "assets" / "pictograms" / "mulberry"
INDEX_PATH = ASSET_DIR.parent / "mulberry_es.json"


def _load_index() -> dict[str, str]:
    entries = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return {normalize_word(keyword): filename for keyword, filename in entries.items()}


INDEX = _load_index()


class MulberryProvider:
    source = "mulberry"
    attribution = "Mulberry Symbols de Steve Lee (mulberrysymbols.org). Licencia: CC BY-SA 4.0"

    async def lookup(self, keyword: str) -> PictogramMatch | None:
        filename = next((INDEX[form] for form in lookup_forms(keyword) if form in INDEX), None)
        if filename is None:
            return None
        base_url = settings.public_base_url.rstrip("/")
        return PictogramMatch(
            source=self.source,
            keyword=keyword,
            pictogram_id=filename.removesuffix(".svg"),
            image_url=f"{base_url}/pictograms/mulberry/{quote(filename)}",
            license="CC BY-SA 4.0",
            commercial_use=True,
        )
