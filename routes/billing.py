from flask import Blueprint, request, jsonify
from database import bookings_col
from bson import ObjectId # Required to query by MongoDB ID




billing_bp = Blueprint('billing', __name__)
from flask import send_file
from utils.pdf_generator import create_invoice_pdf
from models.billing_logic import generate_invoice_data

@billing_bp.route('/download-invoice/<booking_id>', methods=['GET'])
def download_invoice(booking_id):
    # 1. Get the data we built in the previous step
    data = generate_invoice_data(ObjectId(booking_id))
    
    if not data:
        return jsonify({"error": "Booking not found"}), 404
    
    # 2. Generate the physical file
    file_path = create_invoice_pdf(data)
    
    # 3. Send it to the browser
    return send_file(file_path, as_attachment=True)

@billing_bp.route('/add-charge/<booking_id>', methods=['POST'])
def post_extra_charge(booking_id):
    data = request.json
    service = data.get('service') # e.g., "Breakfast"
    amount = data.get('amount')
    
    if add_service_charge(ObjectId(booking_id), service, amount):
        return jsonify({"message": "Charge added successfully"}), 200
    return jsonify({"error": "Failed to add charge"}), 400

@billing_bp.route('/checkout/<booking_id>', methods=['POST'])
def finalize_payment(booking_id):
    """Marks the bill as paid and triggers room status to 'Dirty'"""
    # 1. Update booking status
    bookings_col.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"payment_status": "Paid", "status": "Checked-Out"}}
    )
    
    # 2. Logic to notify housekeeping (handled in previous step)
    # rooms_col.update_one({"room_id": ...}, {"$set": {"status": "Dirty"}})
    
    return jsonify({"message": "Payment finalized. Guest checked out."}), 200