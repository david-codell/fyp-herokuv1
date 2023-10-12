import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marketingTEST import app, db, marketing 
import bcrypt # Import your Flask app, Event model, and any necessary dependencies

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

    def test_get_all_marketing_empty(self):
        # Test the case when there are no events in the database
        response = self.app.get("/marketing/getAll")
        self.assertEqual(response.status_code, 404)
        data = response.json
        self.assertEqual(data["code"], 404)
        self.assertEqual(data["message"], "There are no marketings.")

    def test_get_all_marketing_with_data(self):
        #create some test event in the databse
        with app.app_context():
            # test_event = Event(eventId = 1)
           
            test_marketing = marketing( 
                marketingId=2,
                eventName = "Coldplaydd",
                eventDateTime = "2023-01-01",
                marketingName = "promote taylor swift concert",
                dateStart = "2023-01-02",
                dateEnd = "2023-01-05"   
            )
             
            db.session.add(test_marketing)
            db.session.commit()
        
        #Test the case when there are events in the database
        response = self.app.get("/marketing/getAll") 
        self.assertEqual(response.status_code,200)
        data = response.json
        self.assertEqual(data["code"],200)
        self.assertTrue(isinstance(data["data"], list)) 
        self.assertEqual(len(data["data"]), 1)  

if __name__ == "__main__":
    unittest.main()
