"""Testing FastAPI endpoints.
"""

from fastapi.testclient import TestClient

from app.main import app, this_apis_domain

client = TestClient(app)


def test_help_route():
    """Tests if the '/'-route (help-route) returns correctly data 
    about repositories/developers and built-in documentation.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "repositories": f"{this_apis_domain}/repositories",
        "developers": f"{this_apis_domain}/developers",
        "docs": f"{this_apis_domain}/docs",
        "redoc": f"{this_apis_domain}/redoc",
    }

