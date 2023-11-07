import pytest
from app import create_app, db
from models import User, Summary
from flask_login import current_user

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

@pytest.fixture
def login_user_fixture(client):
    # Create a test user and login before testing
    response = client.post('/login', data={'username': 'testuser', 'password': 'password'})
    assert response.status_code == 302  # Check if it redirects

def test_get_all_summaries(client, init_db, login_user_fixture):
    # Create test summaries in the database
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        summary1 = Summary(
            generated_summary='Summary 1',
            method='Method 1',
            user_id=test_user.user_id
        )
        summary2 = Summary(
            generated_summary='Summary 2',
            method='Method 2',
            user_id=test_user.user_id
        )
        db.session.add(summary1)
        db.session.add(summary2)
        db.session.commit()

    response = client.get('/get-all-summaries')
    assert response.status_code == 200  # Check for success

    data = response.get_json()
    assert len(data) == 2  # Check if it returns the correct number of summaries

def test_get_summary_content(client, init_db, login_user_fixture):
    # Create a test summary in the database
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        summary = Summary(
            generated_summary='Test Summary',
            method='Test Method',
            user_id=test_user.user_id
        )
        db.session.add(summary)
        db.session.commit()

    response = client.get('/get-summary-content/1')  # Assuming summary_id is 1
    assert response.status_code == 200  # Check for success

def test_get_summary_content_unauthorized(client, init_db, login_user_fixture):
    # Create a test summary in the database, but don't associate it with the current user
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        summary = Summary(
            generated_summary='Unauthorized Summary',
            method='Unauthorized Method',
            user_id=test_user.user_id + 1
        )
        db.session.add(summary)
        db.session.commit()

    response = client.get('/get-summary-content/1')  # Assuming summary_id is 1
    assert response.status_code == 403  # Check for unauthorized response

def test_get_summary_content_not_found(client, init_db, login_user_fixture):
    response = client.get('/get-summary-content/1')  # Assuming summary_id is 1
    assert response.status_code == 404  # Check for not found response

def test_delete_summary(client, init_db, login_user_fixture):
    # Create a test summary in the database
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        summary = Summary(
            generated_summary='Test Summary',
            method='Test Method',
            user_id=test_user.user_id
        )
        db.session.add(summary)
        db.session.commit()

    response = client.delete('/delete-summary/1')  # Assuming summary_id is 1
    assert response.status_code == 200  # Check for success

def test_delete_summary_unauthorized(client, init_db, login_user_fixture):
    # Create a test summary in the database, but don't associate it with the current user
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        summary = Summary(
            generated_summary='Unauthorized Summary',
            method='Unauthorized Method',
            user_id=test_user.user_id + 1
        )
        db.session.add(summary)
        db.session.commit()

    response = client.delete('/delete-summary/1')  # Assuming summary_id is 1
    assert response.status_code == 403  # Check for unauthorized response

def test_delete_summary_not_found(client, init_db, login_user_fixture):
    response = client.delete('/delete-summary/1')  # Assuming summary_id is 1
    assert response.status_code == 404  # Check for not found response

def test_summarize_documents(client, init_db, login_user_fixture):
    # Create a test document in the database
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        response = client.post('/summarize', json={'documents': ['Test Content'], 'summarization_method': 'Test Method'})
        assert response.status_code == 200  # Check for success

def test_summarize_documents_no_content(client, init_db, login_user_fixture):
    response = client.post('/summarize', json={'documents': [], 'summarization_method': 'Test Method'})
    assert response.status_code == 400  # Check for bad request response
