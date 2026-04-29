"""Testing FastAPI endpoints.
"""
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app
from app.scraping import UpstreamRequestError

client = TestClient(app)
DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(autouse=True)
def clear_trending_cache():
    """Clears route cache before and after each test."""
    main.clear_trending_cache()
    yield
    main.clear_trending_cache()


def test_help_route():
    """Tests if the '/'-route (help-route) returns correctly data
    about repositories/developers and built-in documentation.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "repositories": "http://testserver/repositories",
        "developers": "http://testserver/developers",
        "docs": "http://testserver/docs",
        "redoc": "http://testserver/redoc",
    }


def test_health_route():
    """Tests if the health route returns application status."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metadata_route():
    """Tests if the metadata route returns API discovery data."""
    response = client.get("/metadata")

    assert response.status_code == 200
    assert response.json() == {
        "name": "GitHub Trending API",
        "version": "1.0.2",
        "docs": "http://testserver/docs",
        "redoc": "http://testserver/redoc",
        "health": "http://testserver/health",
        "repositories": "http://testserver/repositories",
        "developers": "http://testserver/developers",
        "cacheTtlSeconds": 300,
        "supportedDateRanges": ["daily", "weekly", "monthly"],
        "supportedProgrammingLanguagesCount": len(main.AllowedProgrammingLanguages),
        "supportedSpokenLanguagesCount": len(main.AllowedSpokenLanguages),
    }


def test_repositories_route_uses_query_parameters(monkeypatch):
    """Tests the repository endpoint request payload and response parsing."""
    calls = []

    async def fake_get_request(*args, **kwargs):
        calls.append((args, kwargs))
        return (DATA_DIR / "repodata2.html").read_text()

    monkeypatch.setattr(main, "get_request", fake_get_request)

    response = client.get(
        "/repositories",
        params={"since": "weekly", "spoken_language_code": "zh"},
    )

    assert response.status_code == 200
    assert response.json()[0]["repositoryName"] == "v"
    assert calls == [
        (
            ("https://github.com/trending",),
            {
                "compress": True,
                "params": {
                    "since": "weekly",
                    "spoken_language_code": "zh",
                },
            },
        ),
    ]


def test_repositories_route_caches_upstream_html(monkeypatch):
    """Tests repeated requests reuse cached upstream HTML."""
    calls = []

    async def fake_get_request(*args, **kwargs):
        calls.append((args, kwargs))
        return (DATA_DIR / "repodata2.html").read_text()

    monkeypatch.setattr(main, "get_request", fake_get_request)

    first_response = client.get("/repositories", params={"since": "weekly"})
    second_response = client.get("/repositories", params={"since": "weekly"})

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert len(calls) == 1


def test_repositories_language_route_uses_enum_value(monkeypatch):
    """Tests that language enum params are rendered as GitHub URL values."""
    calls = []

    async def fake_get_request(*args, **kwargs):
        calls.append((args, kwargs))
        return (DATA_DIR / "repodata2.html").read_text()

    monkeypatch.setattr(main, "get_request", fake_get_request)

    response = client.get("/repositories/python", params={"since": "monthly"})

    assert response.status_code == 200
    assert response.json()[0]["since"] == "monthly"
    assert calls[0][0] == ("https://github.com/trending/python",)
    assert calls[0][1]["params"] == {"since": "monthly"}


def test_developers_route_uses_query_parameters(monkeypatch):
    """Tests the developer endpoint request payload and response parsing."""
    calls = []

    async def fake_get_request(*args, **kwargs):
        calls.append((args, kwargs))
        return (DATA_DIR / "devdata2.html").read_text()

    monkeypatch.setattr(main, "get_request", fake_get_request)

    response = client.get("/developers", params={"since": "weekly"})

    assert response.status_code == 200
    assert response.json()[0]["username"] == "nunomaduro"
    assert calls == [
        (
            ("https://github.com/trending/developers",),
            {
                "compress": True,
                "params": {"since": "weekly"},
            },
        ),
    ]


def test_developers_language_route_uses_enum_value(monkeypatch):
    """Tests that developer language params use GitHub URL values."""
    calls = []

    async def fake_get_request(*args, **kwargs):
        calls.append((args, kwargs))
        return (DATA_DIR / "devdata2.html").read_text()

    monkeypatch.setattr(main, "get_request", fake_get_request)

    response = client.get("/developers/python", params={"since": "monthly"})

    assert response.status_code == 200
    assert response.json()[0]["since"] == "monthly"
    assert calls[0][0] == ("https://github.com/trending/developers/python",)
    assert calls[0][1]["params"] == {"since": "monthly"}


def test_invalid_query_parameter_returns_validation_error():
    """Tests invalid enum query parameters are rejected by FastAPI."""
    response = client.get("/repositories", params={"since": "yearly"})

    assert response.status_code == 422


def test_invalid_path_parameter_returns_validation_error():
    """Tests invalid enum path parameters are rejected by FastAPI."""
    response = client.get("/repositories/not-a-language")

    assert response.status_code == 422


def test_upstream_request_error_returns_bad_gateway(monkeypatch):
    """Tests upstream request failures are returned as controlled 502s."""

    async def fake_get_request(*args, **kwargs):
        raise UpstreamRequestError("timeout")

    monkeypatch.setattr(main, "get_request", fake_get_request)

    response = client.get("/repositories")

    assert response.status_code == 502
    assert response.json() == {
        "detail": "Unable to fetch GitHub Trending data",
    }


def test_empty_upstream_html_returns_empty_list(monkeypatch):
    """Tests empty upstream HTML returns an empty successful result."""

    async def fake_get_request(*args, **kwargs):
        return ""

    monkeypatch.setattr(main, "get_request", fake_get_request)

    response = client.get("/developers")

    assert response.status_code == 200
    assert response.json() == []


def test_openapi_documents_repository_response_model():
    """Tests repository routes expose a typed response schema."""
    response = client.get("/openapi.json")

    repository_response = response.json()["paths"]["/repositories"]["get"][
        "responses"
    ]["200"]["content"]["application/json"]["schema"]

    assert repository_response == {
        "items": {"$ref": "#/components/schemas/Repository"},
        "title": "Response Trending Repositories Repositories Get",
        "type": "array",
    }


def test_openapi_documents_developer_response_model():
    """Tests developer routes expose a typed response schema."""
    response = client.get("/openapi.json")

    developer_response = response.json()["paths"]["/developers"]["get"][
        "responses"
    ]["200"]["content"]["application/json"]["schema"]

    assert developer_response == {
        "items": {"$ref": "#/components/schemas/Developer"},
        "title": "Response Trending Developers Developers Get",
        "type": "array",
    }
