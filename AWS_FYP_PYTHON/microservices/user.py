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

load_dotenv()

app = Flask(__name__,template_folder="templates")
app.secret_key = 'FYP2023'
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flight_admin:6kKVm7C2PHtVtgGT@esd-g7t6-rds.cs2kfkrucphj.ap-southeast-1.rds.amazonaws.com:3306/flight_booking'
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://admin:Fyp2023!@database-1.cmhw6vxegmhy.ap-southeast-2.rds.amazonaws.com:3306/Fyp2023db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:admin!123@localhost:3306/Fyp2023db'



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 1800}

db = SQLAlchemy(app)




class User(db.Model):
    __tablename__ = 'user'

    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    userType = db.Column(db.Integer, nullable=False)
    passwordSalt = db.Column(db.String(255), nullable=False)
    

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
            "userId": self.userId, 
            "email": self.email, 
            "password": self.password,
            "userType": self.userType, 
            "passwordSalt":self.passwordSalt
        }

class eventGoer(db.Model):
    __tablename__ = 'eventgoer'

    eventGoerId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(255), nullable=False)
    address1 = db.Column(db.String(255), nullable=False)
    address2 = db.Column(db.String(255), nullable=False)

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
            "eventGoerId": self.eventGoerId, 
            "email": self.email, 
            "fname": self.fname,
            "lname": self.lname, 
            "dob":self.dob,
            "phone":self.phone,
            "country":self.country,
            "postal_code":self.postal_code,
            "address1":self.address1,
            "address2":self.address2
        }
        
class eventOrganizer(db.Model):
    __tablename__ = 'eventorganizer'

    eventOrganizerId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    companyName = db.Column(db.String(255), nullable=False)
    UENo = db.Column(db.String(255), nullable=False)
    companyType = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(255), nullable=False)
    address1 = db.Column(db.String(255), nullable=False)
    address2 = db.Column(db.String(255), nullable=False)

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
            "eventGoerId": self.eventGoerId, 
            "email": self.email, 
            "companyName": self.companyName,
            "UENo": self.UENo,
            "companyType": self.companyType, 
            "status":self.status,
            "phone":self.phone,
            "country":self.country,
            "postal_code":self.postal_code,
            "address1":self.address1,
            "address2":self.address2
        }


@app.route("/getAll")
def get_all():
    User_list = User.query.all()
    if len(User_list) > 0:
        return jsonify({ "code": 200, "data": [User.to_dict() for User in User_list] }), 200
    else:
        return jsonify({ "code": 404, "message": "There are no users." }), 404

    
    
@app.route("/create", methods=["POST"])
def create_user():
    data = request.get_json()
 
    if not all(key in data.keys() for key in ('email', 'password', 'userType')):
        return jsonify({"message": "Incorrect JSON object provided."}), 400

    email = data["email"]
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already exists in the database."}), 400

    plaintext_password = data["password"]
    user_type = data["userType"]
    password_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), password_salt)

    try:
        # Create a User record
        Add_User = User(
            email=email,
            password=hashed_password.decode('utf-8'),
            userType=user_type,
            passwordSalt=password_salt
        )
        db.session.add(Add_User)
        db.session.commit()
      
      
        user_id = Add_User.userId
        print("user_id: {}".format(user_id))

        # Check for required fields for eventGoer
        if user_type == '2':
            if not all(key in data.keys() for key in ('fname', 'lname', 'dob', 'phone', 'country', 'postal_code', 'address1', 'address2')):
                return jsonify({"message": "Missing required fields for eventGoer."}), 400

            fname = data["fname"]
            lname = data["lname"]
            dob = data["dob"]
            phone = data["phone"]
            country = data["country"]
            postal_code = data["postal_code"]
            address1 = data["address1"]
            address2 = data["address2"]

            # Create an eventGoer record
            Add_EventGoer = eventGoer(
                userId=user_id,
                email=email,
                fname=fname,
                lname=lname,
                dob=dob,
                phone=phone,
                country=country,
                postal_code=postal_code,
                address1=address1,
                address2=address2
            )
            print(f"Add_EventGoer.userId: {Add_EventGoer.userId}")

            db.session.add(Add_EventGoer)
            db.session.commit()
            
        if user_type == '3':
            if not all(key in data.keys() for key in ('companyName', 'UENo', 'companyType', 'status', 'phone', 'country', 'postal_code', 'address1', 'address2')):
                return jsonify({"message": "Missing required fields for eventOrganizer."}), 400

            companyName = data["companyName"]
            UENo = data["UENo"]
            companyType = data["companyType"]
            status = data["status"]
            phone = data["phone"]
            country = data["country"]
            postal_code = data["postal_code"]
            address1 = data["address1"]
            address2 = data["address2"]
            existing_company = eventOrganizer.query.filter_by(UENo=UENo).first()
            if existing_company:
                return jsonify({"message": "Company already exists in the database."}), 400
                
            Add_EventOrganizer = eventOrganizer(
                email=email,
                companyName=companyName,
                UENo = UENo,
                companyType = companyType,
                status = status,
                phone = phone,
                country = country,
                postal_code = postal_code,
                address1 = address1,
                address2 = address2
            )
            db.session.add(Add_EventOrganizer)
            db.session.commit()
      
        
        return jsonify({"data": Add_User.json(), "code": 201}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": "Email already exists in the database."}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred when adding the user to the database.", "code": 500}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Find the user by email in your database
    user = User.query.filter_by(email=email).first()
    userType = user.userType

    # Check if the user exists
    if user:
        # Retrieve the stored salt from the user object
        stored_salt = user.passwordSalt.encode('utf-8')

        # Hash the input password with the stored salt
        input_password_encoded = bcrypt.hashpw(password.encode('utf-8'), stored_salt)

        # Compare the hashed input password with the stored hashed password
        if input_password_encoded == user.password.encode('utf-8'):
            if userType == 1:
                session["email"] = email
                session["user_type"] = userType
                print(session)
                #render_template('admindashboard.html', sessionEmail=user.email, user_type= userType)
                return jsonify({"message": "Admin login successful", "user_type": 1}), 200
            elif userType == 2:
                return jsonify({"message": "Event Goer login successful", "user_type": 2}), 200
            elif userType == 3:
                return jsonify({"message": "Event Organizer login successful", "user_type": 3}), 200

    # Authentication failed, return an error response
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/getByEmail")
def get_eventOrganizer_by_email():
    args = request.args
    email1 = args.get('email')
    if email1:
        select = eventOrganizer.query.filter_by(email=email1).all()
        if len(select)==1:
            return jsonify({ "code": 200,"data": [eventOrganizer.to_dict() for eventOrganizer in select] }), 200
        else:
            return jsonify({ "code": 404, "message": "No email with this email present in DB." }), 404
    else:
        return jsonify({ "code": 404, "message": "No email provided" }), 404

@app.route("/getByEmail2")
def get_eventGoer_by_email():
    args = request.args
    email1 = args.get('email')
    if email1:
        select = eventGoer.query.filter_by(email=email1).all()
        if len(select)==1:
            return jsonify({ "code": 200,"data": [eventGoer.to_dict() for eventGoer in select] }), 200
        else:
            return jsonify({ "code": 404, "message": "No email with this email present in DB." }), 404
    else:
        return jsonify({ "code": 404, "message": "No email provided" }), 404
    
    

@app.route("/getApproved")
def get_approved_event_organizers():

    # Query the EventOrganizer table for records with 'status' equal to 'not approved'
    approved_event_organizers = eventOrganizer.query.filter_by(status='Approved').all()

    print("Number of 'Approved' EventOrganizers:", len(approved_event_organizers))
    
    if len(approved_event_organizers) > 0:
        # Convert the query results to a list of dictionaries
        return jsonify({ "code": 200, "data": [eventOrganizer.to_dict() for eventOrganizer in approved_event_organizers] }), 200
    else:
        return jsonify({
            "code": 404,
            "message": "No 'not approved' EventOrganizers found."
        }), 404

@app.route("/getNotApproved")
def get_not_approved_event_organizers():

    # Query the EventOrganizer table for records with 'status' equal to 'not approved'
    not_approved_event_organizers = eventOrganizer.query.filter_by(status='Not Approved').all()

    print("Number of 'Not Approved' EventOrganizers:", len(not_approved_event_organizers))
    
    if len(not_approved_event_organizers) > 0:
        # Convert the query results to a list of dictionaries
        return jsonify({ "code": 200, "data": [eventOrganizer.to_dict() for eventOrganizer in not_approved_event_organizers] }), 200
    else:
        return jsonify({
            "code": 404,
            "message": "No 'not approved' EventOrganizers found."
        }), 404
        
@app.route("/getSuspendedEventOrganizers")
def get_suspended_event_organizers():

    # Query the EventOrganizer table for records with 'status' equal to 'not approved'
    not_approved_event_organizers = eventOrganizer.query.filter_by(status='Suspended').all()

    print("Number of 'Suspended' EventOrganizers:", len(not_approved_event_organizers))
    
    if len(not_approved_event_organizers) > 0:
        # Convert the query results to a list of dictionaries
        return jsonify({ "code": 200, "data": [eventOrganizer.to_dict() for eventOrganizer in not_approved_event_organizers] }), 200
    else:
        return jsonify({
            "code": 404,
            "message": "No 'not approved' EventOrganizers found."
        }), 404
    
@app.route("/approveEventOrganizer", methods=["POST"])
def approve_event_organizer():
    email = request.args.get('email')
    status = "Approved"  # Corrected the variable name

    # Check if the event organizer exists by email
    event_organizer = eventOrganizer.query.filter_by(email=email).first()

    if event_organizer:
        try:
            event_organizer.status = status
            db.session.commit()
            return jsonify({"message": "Event organizer approved successfully", "code": 200})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"An error occurred when updating the status: {str(e)}", "code": 500}), 500
    else:
        return jsonify({"message": "Event organizer not found", "code": 404}), 404

@app.route("/suspendEventOrganizer", methods=["POST"])
def suspend_event_organizer():
    email = request.args.get('email')
    status = "Suspended"  # Corrected the variable name

    # Check if the event organizer exists by email
    event_organizer = eventOrganizer.query.filter_by(email=email).first()

    if event_organizer:
        try:
            event_organizer.status = status
            db.session.commit()
            return jsonify({"message": "Event organizer suspended successfully", "code": 200})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"An error occurred when updating the status: {str(e)}", "code": 500}), 500
    else:
        return jsonify({"message": "Event organizer not found", "code": 404}), 404
@app.route("/UnSuspendEventOrganizer", methods=["POST"])
def Unsuspend_event_organizer():
    email = request.args.get('email')
    status = "Approved"  # Corrected the variable name

    # Check if the event organizer exists by email
    event_organizer = eventOrganizer.query.filter_by(email=email).first()

    if event_organizer:
        try:
            event_organizer.status = status
            db.session.commit()
            return jsonify({"message": "Event organizer suspended successfully", "code": 200})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"An error occurred when updating the status: {str(e)}", "code": 500}), 500
    else:
        return jsonify({"message": "Event organizer not found", "code": 404}), 404    

@app.route("/getEventGoers")
def get_all_event_goers():

    # Query the EventOrganizer table for records with 'status' equal to 'not approved'
    event_goers = eventGoer.query.all()

    print("Number of 'Approved' EventOrganizers:", len(event_goers))
    
    if len(event_goers) > 0:
        # Convert the query results to a list of dictionaries
        return jsonify({ "code": 200, "data": [eventGoer.to_dict() for eventGoer in event_goers] }), 200
    else:
        return jsonify({
            "code": 404,
            "message": "No 'not approved' EventOrganizers found."
        }), 404
        
@app.route("/updateEventGoerById", methods=["POST"])
def update_eventgoer_by_id():
    data = request.get_json()
    if 'eventGoerId' not in data:
        return jsonify({"message": "Incorrect JSON object provided"}), 400
    
    eventgoer = eventGoer.query.filter_by(eventGoerId=data["eventGoerId"]).first()

    
    if not eventgoer:
        return jsonify({"message": "eventGoerId is not valid."}), 404
    else:
        try:
            if 'email' in data:
                eventgoer.email = data["email"]
                # Fetch the associated user based on the eventGoer's userId
                user = User.query.filter_by(userId=eventgoer.userId).first()

                if user:
                    user.email = data["email"]
               
            if 'fname' in data:
                eventgoer.fname = data["fname"]
            if 'lname' in data:
                eventgoer.lname = data["lname"]
            if 'dob' in data:
                eventgoer.dob = data["dob"]
            if 'phone' in data:
                eventgoer.phone = data["phone"] 
            if 'country' in data:
                eventgoer.country = data["country"]           
            if 'postal_code' in data:
                eventgoer.postal_code = data["postal_code"]
            if 'address1' in data:
                eventgoer.address1 = data["address1"]
            if 'address2' in data:
                eventgoer.address2 = data["address2"]
            
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred when updating eventgoer data.", "code": 500}), 500
        return {"eventGoerId": data["eventGoerId"], "Success": True, "code": 201}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)