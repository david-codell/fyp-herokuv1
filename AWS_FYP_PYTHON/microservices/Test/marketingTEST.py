import requests
from flask_cors import CORS
from flask import Flask, request, jsonify, session,redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
import bcrypt
from sqlalchemy.exc import IntegrityError  # Import IntegrityError
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()

app = Flask(__name__,template_folder="templates")
app.secret_key = 'FYP2023'
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flight_admin:6kKVm7C2PHtVtgGT@esd-g7t6-rds.cs2kfkrucphj.ap-southeast-1.rds.amazonaws.com:3306/flight_booking'
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://admin:Fyp2023!@database-1.cmhw6vxegmhy.ap-southeast-2.rds.amazonaws.com:3306/Fyp2023db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:admin@localhost:3306/Fyp2023db'



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 1800}

db = SQLAlchemy(app)

class marketing(db.Model):
    __tablename__ = 'marketing'
    
    marketingId= db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(45), nullable=False)
    eventDateTime = db.Column(db.DateTime, nullable=False)
    marketingName = db.Column(db.String(45), nullable=False)
    dateStart = db.Column(db.DateTime, nullable=False)
    dateEnd = db.Column(db.DateTime, nullable=False)    
    
    
    
    def to_dict(self):
        columns = self. __mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self,column)
        return  result
    
    def json(self):
        return{
            "marketingId": self.marketingId,
            "eventName": self.eventName,
            "eventDateTime": self.eventDateTime,
            "marketingName": self.marketingName,
            "dateStart": self.dateStart,
            "dateEnd": self.dateEnd            
        }
        
@app.route("/marketing/create", methods=["POST"])
def create_event():
    
    data = request.get_json()
    print("test marketing now through command line")
    if not all(key in data.keys() for key in ('marketingId', 'eventName')):
        return jsonify({"message": "Incorrect JSON object provided."}), 400


    marketingId = data["marketingId"]
    eventName = data["eventName"]
    eventDateTime = data["eventDateTime"]
    if marketingId == 1:
        try: 
            #extract other data from the reqeuest if marketingId is 1
            marketingName = data["marketingName"]
            dateStart = data["dateStart"]
            dateEnd = data["dateEnd"]            
            
            #create marketing Object
            Add_Marketing = marketing(
                    marketingId=marketingId,
                    eventName =eventName,
                    eventDateTime = eventDateTime,
                    marketingName = marketingName,
                    dateStart = dateStart,
                    dateEnd = dateEnd                            
                )

        
            #add to database
            db.session.add(Add_Marketing)
            db.session.commit()
            
            return jsonify({"data": Add_Marketing.json(), "code": 201}), 201
        
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"message": "Marketing already exists in the database."}), 400
       
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "An error occurred when adding the Marketing to the database.", "code": 500}), 500
        
@app.route("/marketing/suspend/<int:marketingId>", methods=["DELETE"])
def suspend_event(marketingId):
    try:
        marketingRec = marketing.query.get(marketingId)
        print("calling suspend marketing")
        if marketingRec:
            db.session.delete(marketingRec)
            db.session.commit()
            return jsonify({"message": f"Marketing with marketingId {marketingId} has been deleted."}), 200
        else:
            return jsonify({"message": "Marketing not found."}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        # Log the error message for debugging
        app.logger.error(str(e))
        return jsonify({"message": "An error occurred while deleting the Marketing."}), 500
    
@app.route("/marketing/update/<int:marketingId>", methods=["PUT"])
def update_marketing(marketingId):
    
    data = request.get_json()
    if not all(key in data.keys() for key in ('marketingId', 'eventName')):
        return jsonify({"message": "Incorrect JSON object provided."}), 400

    # Retrieve the existing event by its ID
    marketingrec = marketing.query.get(marketingId)
    print(marketingrec.eventName)
    
    if marketingrec:
        try:
            # Update the event attributes with the new data from the JSON payload
            marketingrec.marketingId = data.get("marketingId", marketing.marketingId)
            marketingrec.eventName = data.get("eventName", marketing.eventName)
            marketingrec.eventDateTime = data.get("eventDateTime", marketing.eventDateTime )          
            marketingrec.marketingName = data.get("marketingName", marketing.marketingName)
            marketingrec.dateStart = data.get("dateStart", marketing.dateStart)
            marketingrec.dateEnd = data.get("dateEnd", marketing.dateEnd)
            print("have set markting data for update")
            # Commit the changes to the database
            db.session.commit()
            print("before commit")
            return jsonify({"data": marketing.json(), "message": f"Marketing with marketingId {marketingId} has been updated."}), 200            
            print("after commit")

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "An error occurred when updating the marketing.", "code": 500}), 500
    else:
        return jsonify({"message": "marketing not found."}), 404
            
@app.route("/marketing/getAll")
def get_all():
    marketing_list = marketing.query.all()
    if len(marketing_list) > 0:
        return jsonify({ "code": 200, "data": [marketing.to_dict() for marketing in marketing_list] }), 200
    else:
        return jsonify({ "code": 404, "message": "There are no marketings." }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    
