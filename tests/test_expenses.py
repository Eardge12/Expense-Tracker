import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_jwt_extended import create_access_token
import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client

def test_get_expenses_empty(client):
    response = client.get('/expenses/')
    assert response.status_code == 401

@pytest.fixture
def access_token():
    return create_access_token