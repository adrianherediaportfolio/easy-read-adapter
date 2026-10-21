from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from urllib.request import urlopen

EMOJIBASE_VERSION = "18.0.0"
OPENMOJI_VERSION = "17.0.0"
EMOJIBASE_URL = (
    f"https://cdn.jsdelivr.net/npm/emojibase-data@{EMOJIBASE_VERSION}/es/data.json"
)
OPENMOJI_URL = f"https://cdn.jsdelivr.net/npm/openmoji@{OPENMOJI_VERSION}/data/openmoji.json"
OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "backend"
    / "assets"
    / "pictograms"
    / "openmoji_es.json"
)


def normalize(value: str) -> str:
    folded = unicodedata.normalize("NFD", value.lower())
    return "".join(char for char in folded if unicodedata.category(char) != "Mn")


def words(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", normalize(value))


def tag_values(value: object) -> list[str]:
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, list):
        return [part for part in value if isinstance(part, str) and part.strip()]
    return []


def build_index(emojis: list[dict], available_hexcodes: set[str]) -> dict[str, str]:
    index: dict[str, str] = {}
    for emoji in emojis:
        hexcode = str(emoji.get("hexcode", "")).upper()
        if hexcode not in available_hexcodes:
            continue
        labels = [emoji.get("label", "")]
        labels.extend(tag_values(emoji.get("tags", [])))
        for label in labels:
            if isinstance(label, str):
                for word in words(label):
                    index.setdefault(word, hexcode)
    return dict(sorted(index.items()))


def download_json(url: str) -> list[dict]:
    with urlopen(url, timeout=45) as response:
        return json.load(response)


def main() -> None:
    emojis = download_json(EMOJIBASE_URL)
    openmoji = download_json(OPENMOJI_URL)
    available = {str(item.get("hexcode", "")).upper() for item in openmoji}
    index = build_index(emojis, available)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(index, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {len(index)} Spanish word mappings using "
        f"emojibase-data {EMOJIBASE_VERSION} and OpenMoji {OPENMOJI_VERSION}"
    )


if __name__ == "__main__":
    main()
