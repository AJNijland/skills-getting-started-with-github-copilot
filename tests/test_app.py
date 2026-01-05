import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

def test_signup_for_activity():
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up test@example.com for Chess Club"}

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Programming Class/signup", params={"email": "duplicate@example.com"})
    # Second signup should fail
    response = client.post("/activities/Programming Class/signup", params={"email": "duplicate@example.com"})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test@example.com"})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Redirect
    assert response.headers["location"] == "/static/index.html"