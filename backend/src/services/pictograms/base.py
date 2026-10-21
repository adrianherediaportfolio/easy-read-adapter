from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class PictogramMatch:
    source: str
    keyword: str
    pictogram_id: str
    image_url: str
    license: str
    commercial_use: bool

    def as_dict(self) -> dict[str, str | bool]:
        return {
            "keyword": self.keyword,
            "source": self.source,
            "id": self.pictogram_id,
            "image_url": self.image_url,
            "license": self.license,
            "commercial_use": self.commercial_use,
        }


class PictogramProvider(Protocol):
    source: str
    attribution: str

    async def lookup(self, keyword: str) -> PictogramMatch | None: ...
