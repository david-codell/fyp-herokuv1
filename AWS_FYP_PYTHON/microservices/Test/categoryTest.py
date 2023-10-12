import requests
from flask_cors import CORS
from flask import Flask, request, jsonify, session,redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
import bcrypt
from sqlalchemy.exc import IntegrityError  # Import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

load_dotenv()

app = Flask(__name__,template_folder="templates")
app.secret_key = 'FYP2023'
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flight_admin:6kKVm7C2PHtVtgGT@esd-g7t6-rds.cs2kfkrucphj.ap-southeast-1.rds.amazonaws.com:3306/flight_booking'
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://admin:Fyp2023!@database-1.cmhw6vxegmhy.ap-southeast-2.rds.amazonaws.com:3306/Fyp2023db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:MarcAdriel1!@localhost:3306/Fyp2023db'



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 1800}

db = SQLAlchemy(app)

class Category(db.Model):
    __tablename__ = 'category'

    categoryId = db.Column(db.Integer, primary_key=True)
    categoryType = db.Column(db.String(255), nullable=True)
    categoryName = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {
            "categoryId": self.categoryId, 
            "categoryType": self.categoryType, 
            "categoryName": self.categoryName
           
        }


@app.route("/category/create", methods=["POST"])
def create_category():
    '''
    How to: url - localhost:5000/event/create
    json - {
        
        "organizerId": "12",
        "venueId": "3"
    }
    '''
    data = request.get_json()
    
     
    try:  
        #extract other data from the reqeuest if eventId is 1 
        categoryId = data["categoryId"]
        categoryName = data["categoryName"]
        categoryType = data["categoryType"]
      
        #create Event Object 
        Add_Category = Category( 
                
                categoryId = categoryId,
                categoryName = categoryName,
                categoryType = categoryType             
            )

        # Add to the database
        db.session.add(Add_Category)
        db.session.commit()

        return jsonify({"data": Add_Category.json(), "code": 201}), 201
    except IntegrityError as e:
        # Handle the case when the email is not unique
        db.session.rollback()
        return jsonify({"message": "Email already exists in the database."}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred when adding the user to the database.", "code": 500}), 500

@app.route("/category/suspend/<int:categoryId>", methods=["DELETE"])
def suspend_category(categoryId):
    try:
        category = Category.query.get(categoryId)
        
        if category:
            db.session.delete(category)
            db.session.commit()
            return jsonify({"message": f"Event with categoryId {categoryId} has been deleted."}), 200
        else:
            return jsonify({"message": "Event not found."}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        # Log the error message for debugging
        app.logger.error(str(e))
        return jsonify({"message": "An error occurred while deleting the event."}), 500
    

@app.route("/category/update/<int:categoryId>", methods=["PUT"])
def update_category(categoryId):
    
    data = request.get_json()
    if not all(key in data.keys() for key in ('categoryId', 'categoryName')):
        return jsonify({"message": "Incorrect JSON object provided."}), 400

    # Retrieve the existing event by its ID
    category = Category.query.get(categoryId)
    
    if category:
        try:
            # Update the event attributes with the new data from the JSON payload
            category.categoryId = data.get("categoryId", category.categoryId)
            category.categoryName = data.get("categoryName", category.categoryName)
            category.categoryType = data.get("categoryType", category.categoryType)

            # Commit the changes to the database
            db.session.commit()
            
            return jsonify({"data": category.json(), "message": f"Event with categoryId {categoryId} has been updated."}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "An error occurred when updating the event. Error: " + str(e), "code": 500}), 500
    else:
        return jsonify({"message": "Category not found."}), 404

            
@app.route("/category/getAll")
def get_all():
    Category_list = Category.query.all()
    if len(Category_list) > 0:
        return jsonify({ "code": 200, "data": [Category.to_dict() for Category in Category_list] }), 200
    else:
        return jsonify({ "code": 404, "message": "There are no users." }), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)