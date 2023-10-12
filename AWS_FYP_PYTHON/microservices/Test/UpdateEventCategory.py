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
        #db.session.remove()
        #db.drop_all()

        self.app_context.pop()
        
    def test_update_event(self):
        #Update a event object
        category_data = {
            "categoryId":"1",
            "categoryName":"Rock",
            "categoryType":"Music"

        }
        
        #perform a post request to the /event/create endpoint
        response = self.app.put('/category/update/1', json=category_data)
        data = response.get_json()
        self.assertEqual(data["message"], "Event with categoryId 1 has been updated.")

        self.assertEqual(response.status_code,200)
        self.assertTrue('data' in data)

 

if __name__ == '__main__':
    unittest.main()
