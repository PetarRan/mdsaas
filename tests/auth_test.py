from app import app_factory
from models import db

def test_login():
    app, db = app_factory(config_name='test')
    client = app.test_client()

    # Perform login using client.post() and check the response
    response = client.post("/login", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200

def test_register():
    app, db = app_factory(config_name='test')
    client = app.test_client()

    # Perform registration using client.post() and check the response
    response = client.post("/register", json={"username": "new_user", "password": "new_password", "email": "new@example.com"})
    assert response.status_code == 200