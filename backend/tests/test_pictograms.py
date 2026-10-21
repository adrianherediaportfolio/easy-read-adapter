import json
from pathlib import Path
from xml.etree import ElementTree

import httpx
import pytest
import respx

from src.config import settings
from src.services.pictograms import (
    ARASAAC_API,
    clear_cache,
    pictograms_for_sentences,
    pictograms_with_attributions,
    select_content_words,
)


@pytest.fixture(autouse=True)
def reset_pictogram_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "pictogram_providers", "own,mulberry,openmoji")
    clear_cache()


def test_select_content_words_skips_stopwords_and_limits_results() -> None:
    selected = select_content_words("La niña lee un libro en la escuela.")
    assert len(selected) <= 3
    assert "la" not in selected
    assert "un" not in selected
    assert "libro" in selected


@pytest.mark.asyncio
async def test_own_provider_wins_and_normalizes_accents_plurals_and_verbs() -> None:
    result = await pictograms_for_sentences(["Las niñas leen libros."], enabled=True)
    assert {item["source"] for item in result[0]} == {"own"}
    assert {item["id"] for item in result[0]} == {"nina", "leer", "libro"}


@pytest.mark.asyncio
async def test_mulberry_is_used_when_own_does_not_match(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "pictogram_providers", "own,mulberry")
    result = await pictograms_for_sentences(["El perro camina."], enabled=True)
    assert result[0][0]["source"] == "mulberry"
    assert result[0][0]["id"] == "dog"


@pytest.mark.asyncio
async def test_openmoji_local_index_is_used_as_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "pictogram_providers", "openmoji")
    result = await pictograms_for_sentences(["El perro sonríe."], enabled=True)
    assert result[0][0]["source"] == "openmoji"
    assert result[0][0]["commercial_use"] is True


@pytest.mark.asyncio
@respx.mock
async def test_arasaac_is_not_called_by_default() -> None:
    await pictograms_for_sentences(["La lectura enseña."], enabled=True)
    assert not respx.calls


@pytest.mark.asyncio
@respx.mock
async def test_arasaac_provider_maps_results_when_opted_in(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "pictogram_providers", "arasaac")
    respx.get(f"{ARASAAC_API}/lectura").mock(return_value=httpx.Response(200, json=[{"_id": 1234}]))
    respx.get(f"{ARASAAC_API}/ensena").mock(return_value=httpx.Response(200, json=[]))
    respx.get(f"{ARASAAC_API}/ensenar").mock(return_value=httpx.Response(200, json=[]))
    result = await pictograms_for_sentences(["La lectura enseña."], enabled=True)
    assert result[0][0]["id"] == "1234"
    assert result[0][0]["license"] == "CC BY-NC-SA 4.0"
    assert result[0][0]["commercial_use"] is False


@pytest.mark.asyncio
async def test_attributions_only_include_sources_that_returned_matches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "pictogram_providers", "own,mulberry,openmoji")
    _, attributions = await pictograms_with_attributions(["El niño y el perro."], enabled=True)
    assert attributions == [
        "Mulberry Symbols de Steve Lee (mulberrysymbols.org). Licencia: CC BY-SA 4.0"
    ]


@pytest.mark.asyncio
async def test_disabled_pictograms_make_no_requests() -> None:
    assert await pictograms_for_sentences(["La lectura enseña."], enabled=False) == [[]]


def test_catalog_entries_and_own_svg_documents_are_valid() -> None:
    root = Path(__file__).parents[1] / "assets" / "pictograms"
    own_index = json.loads((root / "own" / "index.json").read_text(encoding="utf-8"))
    mulberry_index = json.loads((root / "mulberry_es.json").read_text(encoding="utf-8"))
    assert all((root / "own" / entry["file"]).is_file() for entry in own_index)
    assert all((root / "mulberry" / filename).is_file() for filename in mulberry_index.values())
    for svg in (root / "own").glob("*.svg"):
        document = ElementTree.parse(svg).getroot()
        assert document.attrib["viewBox"] == "0 0 300 300"
