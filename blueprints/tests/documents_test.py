import pytest
from app import create_app, db
from models import User, Document
import io
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

def test_get_all_documents(client, init_db, login_user_fixture):
    # Create test documents in the database
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        document1 = Document(title='Document 1', content='Content 1', user_id=test_user.user_id)
        document2 = Document(title='Document 2', content='Content 2', user_id=test_user.user_id)
        db.session.add(document1)
        db.session.add(document2)
        db.session.commit()

    response = client.get('/get-all-documents')
    assert response.status_code == 200  # Check for success

    data = response.get_json()
    assert len(data) == 2  # Check if it returns the correct number of documents

def test_delete_document(client, init_db, login_user_fixture):
    # Create a test document in the database
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        document = Document(title='Test Document', content='Test Content', user_id=test_user.user_id)
        db.session.add(document)
        db.session.commit()

    response = client.delete('/delete-document/1')  # Assuming document_id is 1
    assert response.status_code == 200  # Check for success

def test_delete_document_unauthorized(client, init_db, login_user_fixture):
    # Create a test document in the database, but don't associate it with the current user
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        document = Document(title='Unauthorized Document', content='Unauthorized Content', user_id=test_user.user_id + 1)
        db.session.add(document)
        db.session.commit()

    response = client.delete('/delete-document/1')  # Assuming document_id is 1
    assert response.status_code == 403  # Check for unauthorized response

def test_delete_document_not_found(client, init_db, login_user_fixture):
    response = client.delete('/delete-document/1')  # Assuming document_id is 1
    assert response.status_code == 404  # Check for not found response

def test_get_document_content(client, init_db, login_user_fixture):
    # Create a test document in the database
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        document = Document(title='Test Document', content='Test Content', user_id=test_user.user_id)
        db.session.add(document)
        db.session.commit()

    response = client.get('/get-document-content/1')  # Assuming document_id is 1
    assert response.status_code == 200  # Check for success

def test_get_document_content_unauthorized(client, init_db, login_user_fixture):
    # Create a test document in the database, but don't associate it with the current user
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        document = Document(title='Unauthorized Document', content='Unauthorized Content', user_id=test_user.user_id + 1)
        db.session.add(document)
        db.session.commit()

    response = client.get('/get-document-content/1')  # Assuming document_id is 1
    assert response.status_code == 403  # Check for unauthorized response

def test_get_document_content_not_found(client, init_db, login_user_fixture):
    response = client.get('/get-document-content/1')  # Assuming document_id is 1
    assert response.status_code == 404  # Check for not found response

def test_upload_document(client, init_db, login_user_fixture):
    # Create a test document in the database
    with client.application.app_context():
        test_user = User.query.filter_by(username='testuser').first()
        response = client.post('/upload-document', data={'content0': (io.BytesIO(b'Test Content'), 'test.txt')})
        assert response.status_code == 200  # Check for success

        data = response.get_json()
        assert 'document_ids' in data  # Check if it returns document IDs

def test_upload_document_invalid_file(client, init_db, login_user_fixture):
    response = client.post('/upload-document', data={'content0': (io.BytesIO(b'Test Content'), 'test.invalid')})
    assert response.status_code == 400  # Check for bad request response

def test_upload_document_no_content(client, init_db, login_user_fixture):
    response = client.post('/upload-document')
    assert response.status_code == 400  # Check for bad request response
