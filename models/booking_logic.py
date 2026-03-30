from database import bookings_col
from datetime import datetime

def check_availability(room_id, check_in, check_out):
    """
    Returns True if the room is free.
    Prevents 'Double Booking' by checking date overlaps.
    """
    query = {
        "room_id": room_id,
        "status": {"$in": ["Confirmed", "Checked-In"]},
        "$or": [
            {"check_in": {"$lt": check_out}, "check_out": {"$gt": check_in}}
        ]
    }
    overlap = bookings_col.find_one(query)
    return overlap is None

def calculate_total(base_price, check_in, check_out):
    # Converts strings to datetime objects if necessary
    d1 = datetime.strptime(check_in, "%Y-%m-%d")
    d2 = datetime.strptime(check_out, "%Y-%m-%d")
    nights = (d2 - d1).days
    return nights * base_price