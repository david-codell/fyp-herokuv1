from flask import Flask,render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:''@localhost:3306/fyp'
app.secret_key = 'abcd'
db = SQLAlchemy(app)


# Define the Vendor model
class Vendor(db.Model):
    __tablename__ = 'vendor'

    eventid = db.Column(db.Integer, primary_key=True)
    #eventid = db.Column(db.Integer)
    eventname = db.Column(db.String(255))
    eventdatetime = db.Column(db.DateTime)
    eventdescription = db.Column(db.Text)
    venuename = db.Column(db.String(255))
    vendorname = db.Column(db.String(255))
    vendortype = db.Column(db.String(255))

@app.route('/')
def get_vendor_data():
    # Query the vendor table to retrieve the desired data
    vendors = Vendor.query.with_entities(
        Vendor.eventid,
        Vendor.eventname,
        Vendor.eventdatetime,
        Vendor.eventdescription,
        Vendor.venuename,
        Vendor.vendorname,
        Vendor.vendortype
    ).all()

    # Convert the query result to a list of dictionaries
    vendor_data = [
        {
            'eventid': vendor.eventid,
            'eventname': vendor.eventname,
            'eventdatetime': vendor.eventdatetime.isoformat(),  # Convert to ISO format
            'eventdescription': vendor.eventdescription,
            'venuename': vendor.venuename,
            'vendorname': vendor.vendorname,
            'vendortype': vendor.vendortype
        }
        for vendor in vendors
    ]

    # Return the vendor data 
    return render_template('listofvendor.html', vendors=vendors)


@app.route('/editvendor/<int:eventid>', methods=['GET', 'POST'])
def editvendor(eventid):
    vendor = Vendor.query.get(eventid)  # Fetch the vendor data based on the id

    if vendor is None:
        flash('Vendor not found')
        return redirect(url_for('get_vendor_data'))

    return render_template('Viewvendor.html', vendor=vendor)

@app.route('/update/<int:eventid>', methods=['GET', 'POST'])
def update(eventid):
    vendor = Vendor.query.get(eventid)  # Fetch the vendor data based on the eventid
    
    if vendor is None:
        flash('Vendor not found')
        return redirect(url_for('get_vendor_data'))

    if request.method == 'POST':
        # Update the vendor data based on the form submission
        vendor.eventname = request.form['eventname']
        vendor.eventdatetime = request.form['datetime']  # Correct the name attribute
        vendor.eventdescription = request.form['eventdescription']
        vendor.venuename = request.form['venuename']
        vendor.vendorname = request.form['vendorname']
        vendor.vendortype = request.form['vendortype']
        

        # Commit the changes to the database
        db.session.commit()

        flash('Vendor Data Updated Successfully')
        return redirect(url_for('get_vendor_data'))

    return render_template('Viewvendor.html', vendor=vendor)


@app.route('/delete/<int:eventid>')
def delete(eventid):
    vendor_data = Vendor.query.get(eventid)
    db.session.delete(vendor_data)
    db.session.commit()

    flash('Delete Data Success')
    return redirect(url_for('get_vendor_data'))
   
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085, debug=True)