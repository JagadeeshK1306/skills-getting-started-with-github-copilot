import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # (No special setup needed)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act: Sign up
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert: Signup
    assert signup_response.status_code in (200, 400)  # 400 if already signed up

    # Act: Unregister
    unregister_response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert: Unregister
    assert unregister_response.status_code in (200, 404)  # 404 if not found

def test_signup_duplicate():
    # Arrange
    activity = "Programming Class"
    email = "duplicate@mergington.edu"

    # Act: First signup
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act: Duplicate signup
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
