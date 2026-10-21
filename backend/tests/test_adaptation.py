import pytest

from src.config import settings
from src.services.adaptation import adapt_text, simplify_text, split_sentences


def test_rule_simplifier_splits_punctuation_semicolons_and_colons() -> None:
    result = simplify_text("Primera idea; segunda idea: tercera idea. Cuarta idea")

    assert result.splitlines() == [
        "Primera idea",
        "segunda idea",
        "tercera idea.",
        "Cuarta idea",
    ]


def test_rule_simplifier_splits_long_coordinated_clauses() -> None:
    text = (
        "El equipo organiza actividades y ofrece apoyo para que cada estudiante participe, "
        "pero también prepara materiales para las familias y acompaña al alumnado "
        "durante toda la semana en cada actividad del centro."
    )

    sentences = split_sentences(text, "lectura_facil")

    assert len(sentences) > 1
    assert all(sentence.strip() for sentence in sentences)
    assert all("\n" not in sentence for sentence in sentences)


def test_rule_simplifier_removes_blank_lines_and_bullet_prefixes() -> None:
    assert simplify_text("  • Una idea.\n\n- Otra idea.  ") == "Una idea.\nOtra idea."


@pytest.mark.asyncio
async def test_adaptation_uses_offline_rules_without_openai(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "openai_api_key", "  ")

    result, engine = await adapt_text("El grupo aprende. Luego practica.", "lectura_facil")

    assert result == "El grupo aprende.\nLuego practica."
    assert engine == "rules"
