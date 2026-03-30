from datetime import datetime

def is_room_available(db, room_id, check_in, check_out):
    """
    Logic: A room is NOT available if:
    (Requested_CheckIn < Existing_CheckOut) AND (Requested_CheckOut > Existing_CheckIn)
    """
    overlapping_booking = db.bookings.find_one({
        "room_id": room_id,
        "status": {"$ne": "Cancelled"},
        "$and": [
            {"check_in": {"$lt": check_out}},
            {"check_out": {"$gt": check_in}}
        ]
    })
    return overlapping_booking is None
