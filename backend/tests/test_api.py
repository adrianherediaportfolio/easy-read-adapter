from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from pypdf import PdfWriter

from src import database
from src.config import settings
from src.main import app


@pytest.fixture
def api_client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "adaptations.sqlite")
    monkeypatch.setattr(settings, "api_key", "")
    monkeypatch.setattr(settings, "openai_api_key", "")
    with TestClient(app) as client:
        yield client


def test_create_list_get_and_delete_follow_the_api_contract(api_client: TestClient) -> None:
    response = api_client.post(
        "/api/adaptations",
        json={
            "text": "El alumnado participa en actividades.",
            "level": "lectura_facil",
            "pictograms": False,
            "source": "learning-support-hub",
        },
    )

    assert response.status_code == 201
    adaptation = response.json()
    assert set(adaptation) == {
        "id",
        "created_at",
        "level",
        "source",
        "original_text",
        "adapted_text",
        "sentences",
        "readability",
        "engine",
        "attribution",
    }
    assert adaptation["source"] == "learning-support-hub"
    assert adaptation["engine"] == "rules"
    assert adaptation["sentences"] == [
        {"text": "El alumnado participa en actividades.", "pictograms": []}
    ]
    assert adaptation["readability"]["original"]["label"]
    assert adaptation["readability"]["adapted"]["score"] >= 0
    assert "ARASAAC" in adaptation["attribution"]

    summaries = api_client.get("/api/adaptations").json()
    assert summaries == [
        {
            "id": adaptation["id"],
            "created_at": adaptation["created_at"],
            "level": "lectura_facil",
            "preview": adaptation["adapted_text"][:180],
        }
    ]
    assert api_client.get(f"/api/adaptations/{adaptation['id']}").json() == adaptation
    assert api_client.delete(f"/api/adaptations/{adaptation['id']}").status_code == 204
    assert api_client.get(f"/api/adaptations/{adaptation['id']}").status_code == 404


def test_health_is_public_and_reports_openai_status(api_client: TestClient) -> None:
    assert api_client.get("/api/health").json() == {"status": "ok", "ai_enabled": False}


def test_api_key_is_optional_but_protects_adaptation_routes(
    api_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "api_key", "key-for-tests")

    assert api_client.get("/api/health").status_code == 200
    assert api_client.get("/api/adaptations").status_code == 401
    assert api_client.get("/api/adaptations", headers={"X-API-Key": "wrong"}).status_code == 401
    assert (
        api_client.get(
            "/api/adaptations",
            headers={"X-API-Key": "key-for-tests"},
        ).status_code
        == 200
    )


def test_blank_api_key_disables_auth(
    api_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "api_key", "  ")

    assert api_client.get("/api/adaptations").status_code == 200


def test_txt_upload_uses_the_same_adaptation_contract(api_client: TestClient) -> None:
    response = api_client.post(
        "/api/adaptations/upload",
        files={"file": ("texto.txt", "Una frase breve.".encode(), "text/plain")},
        data={"level": "simplificado", "pictograms": "false"},
    )

    assert response.status_code == 201
    assert response.json()["original_text"] == "Una frase breve."
    assert response.json()["level"] == "simplificado"
    assert response.json()["engine"] == "rules"


def test_upload_rejects_files_over_five_megabytes(api_client: TestClient) -> None:
    response = api_client.post(
        "/api/adaptations/upload",
        files={
            "file": (
                "texto.txt",
                b"x" * (5 * 1024 * 1024 + 1),
                "text/plain",
            )
        },
        data={"level": "lectura_facil", "pictograms": "false"},
    )

    assert response.status_code == 413


def test_pdf_without_extractable_text_returns_a_validation_error(api_client: TestClient) -> None:
    buffer = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(buffer)
    buffer.seek(0)

    response = api_client.post(
        "/api/adaptations/upload",
        files={"file": ("vacio.pdf", buffer.getvalue(), "application/pdf")},
        data={"level": "lectura_facil", "pictograms": "false"},
    )

    assert response.status_code == 422


def test_json_text_limit_is_enforced(api_client: TestClient) -> None:
    response = api_client.post(
        "/api/adaptations",
        json={"text": "a" * 20_001, "pictograms": False},
    )

    assert response.status_code == 422
