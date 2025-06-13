import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db
from app import schemas
from .database import (
    create_test_tables,
    drop_test_tables,
    get_test_db,
    TestingSessionLocal
)

# Set up the database once
@pytest.fixture(scope="module")
def test_db():
    create_test_tables()
    yield
    drop_test_tables()

@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
### TESTS ###
def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json().get("message") == "Welcome to the FastAPI Application!"

def test_create_user(client, test_db):
    user_data = {
        "email": "testuser1@gmail.com",
        "password": "testpassword"
    }
    
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    
    response_data = res.json()
    assert "email" in response_data
    assert response_data["email"] == user_data["email"]
    assert "id" in response_data
    assert "created_at" in response_data