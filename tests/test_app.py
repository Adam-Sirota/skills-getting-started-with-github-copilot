import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Fixture to reset activities if needed, but for simplicity, tests are ordered
# Note: In a real app, use a database or reset mechanism

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Sign up a new student
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

    # Verify added
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    # Try to sign up again
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_signup_full_activity():
    # Assuming Chess Club has max 12, add more to fill
    # For simplicity, test with a small activity or adjust data
    # Here, use Gym Class which has 30 max
    for i in range(28):  # Already has 2, add 28 more to reach 30
        email = f"student{i}@mergington.edu"
        response = client.post(f"/activities/Gym%20Class/signup?email={email}")
        if response.status_code != 200:
            break
    # Now try to add one more
    response = client.post("/activities/Gym%20Class/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Activity is full" in data["detail"]

def test_delete_success():
    # First sign up
    client.post("/activities/Programming%20Class/signup?email=delete@mergington.edu")
    # Then delete
    response = client.delete("/activities/Programming%20Class/signup?email=delete@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]

    # Verify removed
    response = client.get("/activities")
    data = response.json()
    assert "delete@mergington.edu" not in data["Programming Class"]["participants"]

def test_delete_not_signed_up():
    response = client.delete("/activities/Chess%20Club/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_delete_invalid_activity():
    response = client.delete("/activities/Invalid%20Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]