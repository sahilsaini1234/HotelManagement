from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hotels' 

db=SQLAlchemy(app)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(50), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Boolean, default=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    room = db.relationship('Room')
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

engine = create_engine('mysql://root:@localhost/hotels') 
Session = sessionmaker(bind=engine)


@app.route('/bookings/create', methods=['GET','POST'])
def create_booking():
    data = request.json
    user_email = data['user_email']
    room_id = data['room_number']
    start_time = datetime.fromisoformat(data['start_time'])
    end_time = datetime.fromisoformat(data['end_time'])

    session = Session()
    
    room = session.query(Room).get(room_id)
    
    if room is None or not room.availability:
        session.close()
        return jsonify({'success': False, 'message': 'Invalid room selection or room not available.'}), 400
    
    if overlap_exists(session, room_id, start_time, end_time):
        session.close()
        return jsonify({'success': False, 'message': 'Overlapping booking exists.'}), 400

    duration_hours = (end_time - start_time).total_seconds() / 3600
    total_price = duration_hours * room.price_per_hour

    booking = Booking(user_email=user_email, room=room, start_time=start_time, end_time=end_time, total_price=total_price)
    room.availability = False  

    session.add(booking)
    session.commit()
    session.close()

    return jsonify({'success': True, 'message': 'Booking created successfully'})

def overlap_exists(session, room_id, start_time, end_time):
    overlap_booking = session.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).first()
    
    return overlap_booking is not None

def overlap_exists_edit(session, room_id, start_time, end_time, booking_id):
    overlap_booking = session.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.start_time < end_time,
        Booking.end_time > start_time,
        Booking.id != booking_id  # Exclude the given booking_id
    ).first()
    return overlap_booking is not None


@app.route('/bookings/edit/<int:booking_id>', methods=['PUT'])
def edit_booking(booking_id):
    data = request.json
    user_email = data['user_email']
    start_time = datetime.fromisoformat(data['start_time'])
    end_time = datetime.fromisoformat(data['end_time'])

    session = Session()
    booking = session.query(Booking).get(booking_id)
    
    if booking is None:
        session.close()
        return jsonify({'success': False, 'message': 'Booking not found.'}), 404
    
    room_id = data['room_number']
    room = session.query(Room).get(room_id)
    
    # if not room.availability:
    #     session.close()
    #     return jsonify({'success': False, 'message': 'Room is no longer available.'}), 400

    if overlap_exists_edit(session, room_id, start_time, end_time,booking_id):
        session.close()
        return jsonify({'success': False, 'message': 'Overlapping booking exists.'}), 400

    duration_hours = (end_time - start_time).total_seconds() / 3600
    total_price = duration_hours * room.price_per_hour

    booking.user_email = user_email
    booking.start_time = start_time
    booking.end_time = end_time
    booking.total_price = total_price
    booking.room_id = room_id

    session.commit()
    session.close()

    return jsonify({'success': True, 'message': 'Booking updated successfully'})


@app.route('/bookings/cancel/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    session = Session()
    booking = session.query(Booking).get(booking_id)
    
    if booking is None:
        session.close()
        return jsonify({'success': False, 'message': 'Booking not found.'}), 404
    
    room = booking.room
    current_time = datetime.now()

    if booking.start_time > current_time + timedelta(hours=48):
        refund_amount = booking.total_price
    elif current_time + timedelta(hours=24) <= booking.start_time <= current_time + timedelta(hours=48):
        refund_amount = booking.total_price / 2
    else:
        refund_amount = 0.0

    room.availability = True
    session.delete(booking)
    session.commit()
    session.close()

    return jsonify({'success': True, 'message': 'Booking canceled successfully', 'refund_amount': refund_amount})

@app.route('/bookings/view', methods=['GET','PUT'])
def view_bookings():
    filters = request.args.to_dict()
    query = db.session.query(Booking)
    print(filters)
    if filters['room_type'] != '':
        room_type = filters['room_type']
        query = query.join(Room).filter(Room.room_type == room_type)
       

    if filters['start_time'] !=  '' and filters['end_time'] != '':
        start_time = datetime.fromisoformat(filters['start_time'])
        end_time = datetime.fromisoformat(filters['end_time'])
        query = query.filter_by(Booking.start_time >= start_time, Booking.end_time <= end_time)

    if filters['user_email'] != '':
        user_email = filters['user_email']
        query = query.filter(Booking.user_email == user_email)
    
    bookings = query.all()
    bookings_list = []
    for booking in bookings:
        bookings_list.append({
            'id': booking.id,
            'user_email': booking.user_email,
            'room_id': booking.room_id,
            'room_type': booking.room.room_type,
            'start_time': booking.start_time.isoformat(),
            'end_time': booking.end_time.isoformat(),
            'total_price': booking.total_price
        })

    return jsonify({'bookings': bookings_list})

if __name__ == '__main__':
    app.run(debug=True)