"""Testing FastAPI endpoints.
"""

from fastapi.testclient import TestClient

from app.main import DOMAIN_NAME, app

client = TestClient(app)


def test_help_route():
    """Tests if the '/'-route (help-route) returns correctly data
    about repositories/developers and built-in documentation.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "repositories": f"{DOMAIN_NAME}/repositories",
        "developers": f"{DOMAIN_NAME}/developers",
        "docs": f"{DOMAIN_NAME}/docs",
        "redoc": f"{DOMAIN_NAME}/redoc",
    }
