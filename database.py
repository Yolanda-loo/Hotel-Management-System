import os
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv() # This loads the variables from the .env file

# Get the URI from environment variables
uri = os.getenv("MONGODB_URI")

# Properly encode the username and password in the URI
if uri and "://" in uri:
    protocol_end = uri.find("://") + 3
    protocol_part = uri[:protocol_end]
    rest = uri[protocol_end:]
    
    # Find the last @ that separates credentials from host (in case password has @)
    at_index = rest.rfind("@")
    
    if at_index != -1:
        credentials = rest[:at_index]
        host_part = rest[at_index + 1:]
        
        if ":" in credentials:
            username, password = credentials.split(":", 1)
            # Only encode if not already encoded (check for % signs)
            if "%" not in credentials:
                encoded_username = quote_plus(username)
                encoded_password = quote_plus(password)
                uri = f"{protocol_part}{encoded_username}:{encoded_password}@{host_part}"
                print(f"DEBUG - Encoded URI: {uri}")

print(f"DEBUG - Final URI: {uri}")
client = MongoClient(uri)

# Define the database and collections
db = client.get_default_database() # This will use 'hotel_db' from the URI
rooms_col = db.rooms
bookings_col = db.bookings
users_col = db.users