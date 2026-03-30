from pymongo import MongoClient
import os

# In production, use os.getenv("MONGO_URI")
client = MongoClient("mongodb://localhost:27017/")
db = client.hotel_db

# Collections handles
rooms_col = db.rooms
bookings_col = db.bookings
guests_col = db.guests