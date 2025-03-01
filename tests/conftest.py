# tests/conftest.py
import pytest
from app import app

@pytest.fixture
def client():
    # Creates a test client for our Flask app
    with app.test_client() as client:
        yield client