import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from userTEST import app, db, User  # Import your Flask app and User model
import bcrypt

class TestYourAPI(unittest.TestCase):
    def setUp(self):
        # Configure the Flask app for testing
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # Use an in-memory SQLite database for testing
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        with app.app_context():
            db.create_all()

            # Create a test user with a hashed password
            password_salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw("testpassword".encode('utf-8'), password_salt)
            test_user = User(email="test1234@example.com", password=hashed_password, userType=1, passwordSalt=password_salt)
            db.session.add(test_user)
            db.session.commit()


    def test_login_success(self):
        with app.app_context():
            # Test a successful login
            input_password = "testpassword"
            input_password_encoded = input_password.encode('utf-8')
            input_password_str = input_password_encoded.decode('utf-8')
            # Test a successful login
            response = self.app.post("/login", json={"email": "test123456@example.com", "password": input_password_str})
            self.assertEqual(response.status_code, 200)
            self.assertIn("Login successful", response.json['message'])

    def test_login_failure(self):
        with app.app_context():
            input_password = "wrongpassword"
            input_password_encoded = input_password.encode('utf-8')
            input_password_str = input_password_encoded.decode('utf-8')
            # Test a failed login with an incorrect password
            response = self.app.post("/login", json={"email": "test@example.com", "password": input_password_str})
            self.assertEqual(response.status_code, 401)
            self.assertIn(b"Invalid credentials", response.data)

            input_password = "testpassword"
            input_password_encoded = input_password.encode('utf-8')
            input_password_str = input_password_encoded.decode('utf-8')

            # Test a failed login with a non-existent user
            response = self.app.post("/login", json={"email": "nonexistent@example.com", "password": input_password_str})
            self.assertEqual(response.status_code, 401)
            self.assertIn(b"Invalid credentials", response.data)

    

if __name__ == "__main__":
    unittest.main()
