import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from userTEST import app, db, User 
import bcrypt # Import your Flask app, User model, and any necessary dependencies

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


    def test_get_all_users_empty(self):
        # Test the case when there are no users in the database
        response = self.app.get("/user/getAll")
        self.assertEqual(response.status_code, 404)
        data = response.json
        self.assertEqual(data["code"], 404)
        self.assertEqual(data["message"], "There are no users.")

    def test_get_all_users_with_data(self):
        # Create some test users in the database
        with app.app_context():
            password_salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw("testpassword".encode('utf-8'), password_salt)
            test_user = User(email="test1234@example.com", password=hashed_password, userType=1, passwordSalt=password_salt)
            test_user2 = User(email="test1234567@example.com", password=hashed_password, userType=1, passwordSalt=password_salt)
            db.session.add(test_user)
            db.session.add(test_user2)
            db.session.commit()

        # Test the case when there are users in the database
        response = self.app.get("/user/getAll")
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data["code"], 200)
        self.assertTrue(isinstance(data["data"], list))
        self.assertEqual(len(data["data"]), 2)  # Assuming two users were added
        # You can add more specific assertions based on your User model attributes

if __name__ == "__main__":
    unittest.main()
