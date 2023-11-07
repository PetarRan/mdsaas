import pytest
from app import create_app, db
from models import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

def test_login_valid_user(app, client, init_db):
    # Create a test user in the database
    with app.app_context():
        test_user = User(username='testuser', password='password')
        db.session.add(test_user)
        db.session.commit()

    response = client.post('/login', data={'username': 'testuser', 'password': 'password'})
    assert response.status_code == 302  # Check if it redirects

def test_login_invalid_user(client):
    response = client.post('/login', data={'username': 'nonexistent', 'password': 'wrongpass'})
    assert response.status_code == 401  # Check for unauthorized response

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302  # Check if it redirects

def test_register_new_user(client):
    response = client.post('/register', data={'username': 'newuser', 'password': 'newpass', 'email': 'newuser@example.com'})
    assert response.status_code == 302  # Check if it redirects

def test_register_existing_user(app, client, init_db):
    # Create a test user in the database
    with app.app_context():
        test_user = User(username='existinguser', password='password')
        db.session.add(test_user)
        db.session.commit()

    response = client.post('/register', data={'username': 'existinguser', 'password': 'password', 'email': 'existing@example.com'})
    assert response.status_code == 400  # Check for a bad request response
