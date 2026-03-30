from flask import Flask
from routes.bookings import booking_bp
from routes.auth import auth_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(booking_bp, url_prefix='/api/bookings')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

if __name__ == '__main__':
    print("Server running on http://localhost:5000")
    app.run(debug=True)