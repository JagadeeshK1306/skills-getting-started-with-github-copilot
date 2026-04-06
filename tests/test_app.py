import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code in (200, 400)  # 400 if already signed up
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code in (200, 404)  # 404 if not found

def test_signup_duplicate():
    activity = "Programming Class"
    email = "duplicate@mergington.edu"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Duplicate signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
