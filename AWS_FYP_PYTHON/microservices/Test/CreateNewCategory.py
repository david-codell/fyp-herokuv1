import unittest
from categoryTest import app, db, Category

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

    def test_create_event(self):
        # Create a user object
        event_data = {
           "categoryId":"1"
           ,
           "categoryType":"Sports"
           ,
           "categoryName":"Basketball"
          }
        # Perform a POST request to the /user/create endpoint
        response = self.app.post('/category/create', json=event_data)
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertTrue('data' in data)
    
    

if __name__ == '__main__':
    unittest.main()
