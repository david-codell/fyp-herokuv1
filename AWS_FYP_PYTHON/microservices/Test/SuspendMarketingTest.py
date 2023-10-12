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
        
    def test_suspend_event(self):
        #Suspends a event object

        
        #perform a suspend reuqest to the /event/suspend endpoint
        response = self.app.delete('/marketing/suspend/1')
        
        self.assertIn(response.status_code, [200, 404])
        
        # Check the response message
        if response.status_code == 200:
            response_data = response.get_json()
            self.assertEqual(response_data["message"], "Marketing with marketingId 1 has been deleted.")
        elif response.status_code == 404:
            self.assertEqual(response_data["message"], "Marketing not found.")
 

if __name__ == '__main__':
    unittest.main()
