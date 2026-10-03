from fastapi.testclient import TestClient
from api.main import app
client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_search_validates_short_query():
    response = client.get("/search?q=x")
    assert response.status_code == 422

def test_products_validates_page():
    response = client.get("/products?page=99")
    assert response.status_code == 422
