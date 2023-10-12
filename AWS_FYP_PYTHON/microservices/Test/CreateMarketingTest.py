import unittest
from marketingTEST import app, db, marketing

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
        #db.session.remove()
        #db.drop_all()

        self.app_context.pop()
        
    def test_create_marketing(self):
        #Create a marketing object
       
        marketing_data = {
            "marketingId": 1,
            "eventName": "black pink concert",
            "eventDateTime": "2023-01-01",
            "marketingName": "promote black pink concert",
            "dateStart": "2023-01-02",
            "dateEnd": "2023-01-05"           
        }
        
        #perform a post reuqest to the /marketing/create endpoint
        response = self.app.post('/marketing/create', json=marketing_data)
        data =response.get_json()
        self.assertEqual(response.status_code,201)
        self.assertTrue('data' in data)

if __name__ == '__main__':
    unittest.main()
