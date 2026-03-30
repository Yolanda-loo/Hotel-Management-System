from flask import Blueprint, request, jsonify
from database import bookings_col, rooms_col
from models.booking_logic import check_availability, calculate_total
from datetime import datetime

booking_bp = Blueprint('bookings', __name__)

@booking_bp.route('/create', methods=['POST'])
def book_room():
    data = request.json
    room_id = data.get('room_id')
    
    # 1. Get Room Price
    room = rooms_col.find_one({"room_id": room_id})
    if not room:
        return jsonify({"error": "Room not found"}), 404

    # 2. Prevent Double Booking
    if not check_availability(room_id, data['check_in'], data['check_out']):
        return jsonify({"error": "Room is already booked for these dates"}), 400

    # 3. Build Booking Document
    new_booking = {
        "guest_id": data['guest_id'],
        "room_id": room_id,
        "check_in": data['check_in'],
        "check_out": data['check_out'],
        "total_bill": calculate_total(room['price_per_night'], data['check_in'], data['check_out']),
        "status": "Confirmed",
        "created_at": datetime.now()
    }

    result = bookings_col.insert_one(new_booking)
    return jsonify({"message": "Booking successful", "id": str(result.inserted_id)}), 201