from pymongo import MongoClient
from flask_bcrypt import Bcrypt

# Initialize
client = MongoClient("mongodb://localhost:27017/")
db = client.hotel_db
bcrypt = Bcrypt()

def seed_data():
    print("Deleting old data...")
    db.rooms.delete_many({})
    db.users.delete_many({})

    # 1. Seed Rooms
    rooms = [
        {"room_id": "101", "type": "Standard", "price_per_night": 800, "status": "Clean", "amenities": ["WiFi", "TV"]},
        {"room_id": "102", "type": "Standard", "price_per_night": 800, "status": "Dirty", "amenities": ["WiFi", "TV"]},
        {"room_id": "201", "type": "Deluxe", "price_per_night": 1500, "status": "Clean", "amenities": ["WiFi", "Mini Bar", "Sea View"]},
        {"room_id": "301", "type": "Suite", "price_per_night": 3000, "status": "Maintenance", "amenities": ["WiFi", "Kitchen", "Jacuzzi"]}
    ]
    db.rooms.insert_many(rooms)
    print(f"Inserted {len(rooms)} rooms.")

    # 2. Seed Admin User
    admin_password = "AdminPassword123"
    hashed_pw = bcrypt.generate_password_hash(admin_password).decode('utf-8')
    
    admin_user = {
        "username": "admin",
        "password": hashed_pw,
        "role": "Manager",
        "full_name": "Tebogo Mathaba"
    }
    db.users.insert_one(admin_user)
    print("Admin user created: username 'admin', password 'AdminPassword123'")

if __name__ == "__main__":
    seed_data()