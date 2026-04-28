"""Testing FastAPI endpoints.
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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
