import unittest
from userTEST import app, db, User

class TestYourAPI(unittest.TestCase):

    def setUp(self):
        # Create an application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Create a test client for making requests
        self.app = app.test_client()

        # Set up a test database (in-memory SQLite)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()

    def tearDown(self):
        # Clean up the test database after each test
        # db.session.remove()
        # db.drop_all()

        self.app_context.pop()

    def test_create_eventGoer(self):
        # Create a user object
        user_data = {
            "email": "eventGoer@example.com",
            "password": "password123",
            "userType": 2,
            "fname": "John",
            "lname": "Doe",
            "dob": "1990-01-01",
            "phone": "1234567890",
            "country": "USA",
            "postal_code": "12345",
            "address1": "123 Main St",
            "address2": "Apt 4B"
        }
        # Perform a POST request to the /user/create endpoint
        response = self.app.post('/user/create', json=user_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertTrue('data' in data)
    
    def test_create_eventOrganizer(self):
        # Create a user object
        user_data = {
            "email": "eventOrganizer@example.com",
            "password": "password123",
            "userType": 3,
            "companyName": "TESTCOMPANY",
            "UENo": "12345678A",
            "companyType": "TEST",
            "status": "Not Appoved",
            "phone": "1234567890",
            "country": "USA",
            "postal_code": "12345",
            "address1": "123 Main St",
            "address2": "Apt 4B"
        }
        # Perform a POST request to the /user/create endpoint
        response = self.app.post('/user/create', json=user_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertTrue('data' in data)
    

if __name__ == '__main__':
    unittest.main()
