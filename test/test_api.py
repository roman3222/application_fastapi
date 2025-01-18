from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_item():
    data = {"user_name": "New Item", "description": "ololo"}
    response = client.post("/applications/", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["user_name"] == "New Item"
    assert response_data["description"] == "ololo"