from app import app_factory
from flask_sqlalchemy import SQLAlchemy

def test_user_insertion():
    app, db, User = app_factory(config_name='test')
    with app.app_context():
        db.create_all()

        user = User(user_id=129834, username='test_user', password='test_password', email='test@example.com', registration_date="2023-10-26 00:00:00.000")
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username='test_user').first()
        assert retrieved_user is not None
        assert retrieved_user.username == 'test_user'
        
        db.session.delete(user)
        db.session.commit()
        retrieved_user = User.query.filter_by(username='test_user').first()
        assert retrieved_user is None
        #todo the created test user should be deleted after the test