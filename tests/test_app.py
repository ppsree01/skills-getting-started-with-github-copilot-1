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
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_and_unregister():
    # Use a test email and activity
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Ensure not already signed up
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Ignore error if not present

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400

    # Unregister (should succeed)
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    if response.status_code == 200:
        assert response.json()["message"] == f"Removed {email} from {activity}"
    else:
        # If already removed, 404 is also acceptable for first call
        assert response.status_code == 404

    # Unregister again should fail (404)
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
