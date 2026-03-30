from flask import Blueprint, request, jsonify
from database import db
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = db.users.find_one({"username": username})

    if user and bcrypt.check_password_hash(user['password'], password):
        # In a full app, you'd return a JWT token here
        return jsonify({
            "message": "Login successful",
            "user": {
                "username": user['username'],
                "role": user['role'],
                "name": user['full_name']
            }
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401