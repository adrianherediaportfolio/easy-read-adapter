import pytest

from src.services.readability import calculate_readability, count_syllables, readability_label


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("casa", 2),
        ("educación", 4),
        ("país", 2),
        ("pingüino", 3),
        ("guitarra", 3),
        ("queso", 2),
    ],
)
def test_spanish_syllable_counter(word: str, expected: int) -> None:
    assert count_syllables(word) == expected


def test_inflesz_formula_for_known_text() -> None:
    result = calculate_readability("Hola, mundo.")

    assert result == {"score": 80.24, "label": "muy fácil"}


@pytest.mark.parametrize(
    ("score", "label"),
    [
        (39.99, "muy difícil"),
        (40, "algo difícil"),
        (55, "normal"),
        (65, "bastante fácil"),
        (80, "muy fácil"),
    ],
)
def test_inflesz_labels(score: float, label: str) -> None:
    assert readability_label(score) == label


def test_empty_text_has_a_defined_readability_result() -> None:
    assert calculate_readability("") == {"score": 0.0, "label": "muy difícil"}
