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

class Venue(db.Model):
    __tablename__ = 'venue'
    
    venueId = db.Column(db.Integer, primary_key=True)
    venueName = db.Column(db.String(45), nullable=False)
    capacity = db.Column(db.Integer, nullable=True)
    postalcode = db.Column(db.Integer, nullable=True)
    address1 = db.Column(db.String(45), nullable=False)
    address2 = db.Column(db.String(45), nullable=False)
    
    def to_dict(self):
        columns = self. __mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self,column)
        return  result
    
    def json(self):
        return{
            "venueId": self.venueId,
            "venueName": self.venueName,
            "capacity": self.capacity,
            "postalcode": self.postalcode,
            "address1": self.address1,
            "address2": self.address2,
        }
        
@app.route("/create", methods=["POST"])
def create_venue():
    data = request.get_json()
    
    if not all(key in data.keys() for key in ('venueName', 'capacity', 'postalcode', 'address1', 'address2')):
        return jsonify({"message": "Incorrect JSON object provided."}), 400

    try: 
        venueName = data["venueName"]
        capacity = data["capacity"]
        postalcode = data["postalcode"]
        address1 = data["address1"]
        address2 = data["address2"]
            
        #create Venue Object
        Add_Venue = Venue(
                venueName =venueName,
                capacity = capacity,
                postalcode = postalcode,
                address1 = address1,
                address2 = address2,
            
            )

        #add to database
        db.session.add(Add_Venue)
        db.session.commit()
            
        return jsonify({"data": Add_Venue.json(), "code": 201}), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Venue already exists in the database"}), 400
       
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred when adding the venue to the database", "code": 500}), 500
        
@app.route("/suspend/<int:venueId>", methods=["DELETE"])
def suspend_venue(venueId):
    try:
        venue = Venue.query.get(venueId)
        
        if venue:
            db.session.delete(venue)
            db.session.commit()
            return jsonify({"message": f"Venue with venueId {venueId} has been deleted."}), 200
        else:
            return jsonify({"message": "Venue not found."}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        # Log the error message for debugging
        app.logger.error(str(e))
        return jsonify({"message": "An error occurred while deleting the venue."}), 500
    
@app.route("/update/<int:venueId>", methods=["PUT"])
def update_venue(venueId):
    
    data = request.get_json()
    
    # Check if the required fields are present in the JSON payload
    if not all(key in data.keys() for key in ('venueName', 'capacity', 'postalcode', 'address1', 'address2')):
        return jsonify({"message": "Incorrect JSON object provided."}), 400

    # Retrieve the existing Venue by its ID
    venue = Venue.query.get(venueId)
    
    if venue:
        try:
            # Update the Venue attributes with the new data from the JSON payload
            venue.venueName = data.get("venueName", venue.venueName)
            venue.capacity = data.get("capacity", venue.capacity)
            venue.postalcode = data.get("postalcode", venue.postalcode)
            venue.address1 = data.get("address1", venue.address1)
            venue.address2 = data.get("address2", venue.address2)

            # Commit the changes to the database
            db.session.commit()
            
            return jsonify({"data": venue.json(), "message": f"Venue with venueId {venueId} has been updated."}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "An error occurred when updating the venue.", "code": 500}), 500
    else:
        return jsonify({"message": "Venue not found."}), 404
            
@app.route("/getAll")
def get_all():
    Venue_list = Venue.query.all()
    if len(Venue_list) > 0:
        return jsonify({ "code": 200, "data": [Venue.to_dict() for Venue in Venue_list] }), 200
    else:
        return jsonify({ "code": 404, "message": "There are no venue." }), 404
    

    
@app.route("/getVenueById")
def get_venue_by_venueid():
    
    args = request.args
    venue1 = args.get('venueId')
    
    # Use venueId directly as a parameter, no need to use request.args.get
    select = Venue.query.filter_by(venueId=venue1).all()
    if len(select) == 1:
        return jsonify({ "code": 200, "data": [Venue.to_dict() for Venue in select] }), 200
    else:
        return jsonify({ "code": 404, "message": "No venue with this venueId present in DB." }), 404

'''@app.route("/venue/updateVenueById", methods=["POST"])
def update_venue_by_id():
    data = request.get_json()
    if not all(key in data.keys() for key in ('venueId','venueName')):
        return jsonify({"message": "Incorrect JSON object provided"}),500
    
    if data["venueName"].replace(" ","")=="":
        return jsonify({"message": "Venue name canot be blank or contain only whitespace"}),500
    
    has_alphabet = False
    cur_venue_name=data["venueName"].lower()
    for ch in "abcdefghijklmnopqrstuvwxyz":
        if ch in cur_venue_name:
            has_alphabet=True
            break    
        
    if not has_alphabet:
        return jsonify({ "message": "Venue name has no alphabet" }), 500

    if not cur_venue_name[0].isalpha():
        return jsonify({ "message": "Venue name cannot start with number or symbol" }), 500

    venue = Venue.query.filter_by(venueId=data["venueId"]).first()

    if not venue:
        return jsonify({ "message": "VenueID is not valid." }), 500
    else:
        try:
            cur_venue=db.session.query(Venue).get(data["venueId"])
            cur_venue.venueName = data["venueName"]
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred when updating venue name.", "code":500})
        return { "venueId": data["venueId"],"Success":True, "code": 201 }'''

@app.route("/updateVenueById", methods=["POST"])
def update_venue_by_id():
    data = request.get_json()
    if 'venueId' not in data:
        return jsonify({"message": "Incorrect JSON object provided"}), 400
    
    venue = Venue.query.filter_by(venueId=data["venueId"]).first()

    if not venue:
        return jsonify({"message": "VenueID is not valid."}), 404
    else:
        try:
            if 'venueName' in data:
                venue.venueName = data["venueName"]
            if 'capacity' in data:
                venue.capacity = data["capacity"]
            if 'postalcode' in data:
                venue.postalcode = data["postalcode"]
            if 'address1' in data:
                venue.address1 = data["address1"]
            if 'address2' in data:
                venue.address2 = data["address2"]
            
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred when updating venue data.", "code": 500}), 500
        return {"venueId": data["venueId"], "Success": True, "code": 201}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
    
