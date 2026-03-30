from database import bookings_col
from datetime import datetime

def add_service_charge(booking_id, service_name, amount):
    """Adds a line item to the guest's bill (e.g., Laundry: $20)"""
    service_item = {
        "service": service_name,
        "amount": amount,
        "date": datetime.now()
    }
    
    # Use MongoDB's $push to append to an array of services
    result = bookings_col.update_one(
        {"_id": booking_id},
        {
            "$push": {"extra_services": service_item},
            "$inc": {"total_bill": amount} # Increment the total bill automatically
        }
    )
    return result.modified_count > 0

def generate_invoice_data(booking_id):
    """Aggregates all charges for the final checkout screen"""
    booking = bookings_col.find_one({"_id": booking_id})
    if not booking:
        return None
        
    # Logic to format the data for a frontend 'Invoice' component
    return {
        "guest_id": booking['guest_id'],
        "room_id": booking['room_id'],
        "stay_dates": f"{booking['check_in']} to {booking['check_out']}",
        "room_charge": booking.get('room_charge', 0),
        "extras": booking.get('extra_services', []),
        "grand_total": booking.get('total_bill', 0),
        "status": booking.get('payment_status', 'Pending')
    }