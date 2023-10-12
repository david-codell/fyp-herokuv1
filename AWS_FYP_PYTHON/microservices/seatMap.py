from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:''@localhost:3306/fyp'
app.secret_key = 'abcd'
db = SQLAlchemy(app)

# Define the Event model
class Event(db.Model):
    __tablename__ = 'vieweventseapmap'

    eventid = db.Column(db.Integer, primary_key=True)
    eventname = db.Column(db.String(255))
    eventdatetime = db.Column(db.DateTime)
    eventdescription = db.Column(db.Text)
    venuename = db.Column(db.String(255))
    capacity = db.Column(db.Integer())
    address = db.Column(db.String(255))
    status = db.Column(db.String(255))

@app.route('/')
def get_event_data():
    events = Event.query.all()
    event_data = [
        {
            'eventid': event.eventid,
            'eventname': event.eventname,
            'eventdatetime': event.eventdatetime.isoformat() if event.eventdatetime else None,
            'eventdescription': event.eventdescription,
            'venuename': event.venuename,
            'capacity': event.capacity,
            'address': event.address,
            'status': event.status
        }
        for event in events
    ]
    return render_template('Viewandeditseatmaplist.html', events=event_data)

@app.route('/editseatmap/<int:eventid>', methods=['GET', 'POST'])
def editseatmap(eventid):
    event = Event.query.get(eventid)
    if event is None:
        flash('Event not found')
        return redirect(url_for('get_event_data'))

    return render_template('Editseatmapprice.html', event=event)

@app.route('/update/<int:eventid>', methods=['POST'])
def update_eventdata(eventid):
    event = Event.query.get(eventid)
    if event is None:
        flash('Event not found')
        return redirect(url_for('get_event_data'))

    if request.method == 'POST':
        event.eventname = request.form['eventname']
        event.eventdatetime = request.form['eventdatetime']
        event.eventdescription = request.form['eventdescription']
        event.venuename = request.form['venuename']
        event.capacity = request.form['capacity']
        event.address = request.form['address']
        event.status = request.form['status']
        db.session.commit()
        flash('Event Data Updated Successfully')
        return redirect(url_for('get_event_data'))

    return render_template('Editseatmapprice.html', event=event)

@app.route('/filter_events', methods=['GET'])
def filter_events():
    # Get filtering criteria from the user input
    category = request.args.get('category')
    status = request.args.get('status')

    # Build the query for filtering events based on criteria
    query = Event.query

    if category:
        query = query.filter(Event.category == category)

    if status:
        query = query.filter(Event.status == status)

    # Execute the query and retrieve the filtered events
    filtered_events = query.all()

    # Prepare the filtered event data for rendering
    event_data = [
        {
            'eventid': event.eventid,
            'eventname': event.eventname,
            'eventdatetime': event.eventdatetime.isoformat() if event.eventdatetime else None,
            'eventdescription': event.eventdescription,
            'venuename': event.venuename,
            'capacity': event.capacity,
            'address': event.address,
            'status': event.status
        }
        for event in filtered_events
    ]

    return render_template('filtered_events.html', events=event_data)
    
# Define the SeatPrice model
class SeatPrice(db.Model):
    __tablename__ = 'seatprice'
    
    eventid = db.Column(db.Integer, db.ForeignKey('vieweventseapmap.eventid'), primary_key=True)
    cat1 = db.Column(db.Integer)
    cat2 = db.Column(db.Integer)
    cat3 = db.Column(db.Integer)
    cat4 = db.Column(db.Integer)
    cat1_capacity = db.Column(db.Integer)
    cat2_capacity = db.Column(db.Integer)
    cat3_capacity = db.Column(db.Integer)
    cat4_capacity = db.Column(db.Integer)
    
    # Define a relationship to the Event model
    event = db.relationship('Event', backref='seatprices')

@app.route('/update_seatmap_prices/<int:eventid>', methods=['POST'])
def update_seatmap_prices(eventid):
    event = Event.query.get(eventid)
    
    if request.method == 'POST':
        seatprice_category1 = request.form['cat1']
        seatprice_category2 = request.form['cat2']
        seatprice_category3 = request.form['cat3']
        seatprice_category4 = request.form['cat4']
        seatprice_category1_capacity = request.form['cat1_capacity']
        seatprice_category2_capacity = request.form['cat2_capacity']
        seatprice_category3_capacity = request.form['cat3_capacity']
        seatprice_category4_capacity = request.form['cat4_capacity']

        # Check if seat prices for this event already exist
        seat_prices = SeatPrice.query.filter_by(eventid=event.eventid).first()

        if seat_prices:
            # If seat prices for this event exist, update them
            seat_prices.cat1 = seatprice_category1
            seat_prices.cat2 = seatprice_category2
            seat_prices.cat3 = seatprice_category3
            seat_prices.cat4 = seatprice_category4
            seat_prices.cat1_capacity = seatprice_category1_capacity
            seat_prices.cat2_capacity = seatprice_category2_capacity
            seat_prices.cat3_capacity = seatprice_category3_capacity
            seat_prices.cat4_capacity = seatprice_category4_capacity
        else:
            # If seat prices don't exist, create a new entry
            seat_prices = SeatPrice(
                eventid=event.eventid,
                cat1=seatprice_category1,
                cat2=seatprice_category2,
                cat3=seatprice_category3,
                cat4=seatprice_category4,
                cat1_capacity=seatprice_category1_capacity,
                cat2_capacity=seatprice_category2_capacity,
                cat3_capacity=seatprice_category3_capacity,
                cat4_capacity=seatprice_category4_capacity
            )
            db.session.add(seat_prices)

        db.session.commit()

    # Fetch seat prices for the specified event
    seat_prices = SeatPrice.query.filter_by(eventid=eventid).first()
    

    # Render the same template with the updated data
    return render_template('Editseatmapprice.html', event=event, seat_prices=seat_prices)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086, debug=True)
