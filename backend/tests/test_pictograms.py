import httpx
import pytest
import respx

from src.services.pictograms import (
    ARASAAC_API,
    ARASAAC_IMAGE,
    clear_cache,
    pictograms_for_sentences,
    select_content_words,
)


def test_select_content_words_skips_stopwords_and_limits_results() -> None:
    selected = select_content_words("La niña lee un libro en la escuela.")

    assert len(selected) <= 3
    assert "la" not in selected
    assert "un" not in selected
    assert "libro" in selected


@pytest.mark.asyncio
@respx.mock
async def test_arasaac_results_are_mapped_to_image_urls() -> None:
    clear_cache()
    respx.get(f"{ARASAAC_API}/lectura").mock(return_value=httpx.Response(200, json=[{"_id": 1234}]))
    respx.get(f"{ARASAAC_API}/ense%C3%B1a").mock(return_value=httpx.Response(200, json=[]))

    result = await pictograms_for_sentences(["La lectura enseña."], enabled=True)

    assert result == [
        [
            {
                "keyword": "lectura",
                "arasaac_id": 1234,
                "image_url": ARASAAC_IMAGE.format(id=1234),
            }
        ]
    ]


@pytest.mark.asyncio
@respx.mock
async def test_arasaac_failure_does_not_fail_the_adaptation() -> None:
    clear_cache()
    respx.get(f"{ARASAAC_API}/lectura").mock(
        return_value=httpx.Response(503, json={"message": "unavailable"})
    )
    respx.get(f"{ARASAAC_API}/ense%C3%B1a").mock(
        return_value=httpx.Response(503, json={"message": "unavailable"})
    )

    assert await pictograms_for_sentences(["La lectura enseña."], enabled=True) == [[]]


@pytest.mark.asyncio
async def test_disabled_pictograms_make_no_network_requests() -> None:
    assert await pictograms_for_sentences(["La lectura enseña."], enabled=False) == [[]]
