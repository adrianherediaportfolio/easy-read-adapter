import json
from pathlib import Path
from urllib.parse import quote

from .base import PictogramMatch
from .normalization import lookup_forms, normalize_word

INDEX_PATH = Path(__file__).resolve().parents[3] / "assets" / "pictograms" / "openmoji_es.json"
OPENMOJI_VERSION = "17.0.0"


def _load_index() -> dict[str, str]:
    entries = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return {normalize_word(keyword): hexcode for keyword, hexcode in entries.items()}


INDEX = _load_index()


class OpenMojiProvider:
    source = "openmoji"
    attribution = (
        "Emojis de OpenMoji, proyecto de emojis e iconos de código abierto "
        "(openmoji.org). Licencia: CC BY-SA 4.0"
    )

    async def lookup(self, keyword: str) -> PictogramMatch | None:
        hexcode = next((INDEX[form] for form in lookup_forms(keyword) if form in INDEX), None)
        if hexcode is None:
            return None
        image_url = (
            "https://cdn.jsdelivr.net/npm/openmoji@"
            f"{OPENMOJI_VERSION}/color/svg/{quote(hexcode)}.svg"
        )
        return PictogramMatch(
            source=self.source,
            keyword=keyword,
            pictogram_id=hexcode,
            image_url=image_url,
            license="CC BY-SA 4.0",
            commercial_use=True,
        )
