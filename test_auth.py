import unittest
from flask import Flask, session
from app import app  # Replace with the actual import for your Flask app
from models import db, User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Create a test client
        self.app.testing = True  # Set the app to testing mode

        with app.app_context():
            db.create_all()  # Create the database tables

    def tearDown(self):
        with app.app_context():
            db.drop_all()  # Drop the database tables

    def test_login(self):
        # Test the login functionality
        data = {
            "username": "testuser",
            "password": "testpassword"
        }

        response = self.app.post("/login", json=data)
        user = User
        self.assertEqual(response.status_code, 200)
        self.assertEqual(session.get("user_id"), user.user_id)  # Check if user is logged in

    def test_register(self):
        # Test the registration functionality
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com"
        }

        response = self.app.post("/register", json=data)

        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(username=data["username"]).first()
        self.assertIsNotNone(user)  # Check if user was successfully registered

if __name__ == '__main__':
    unittest.main()