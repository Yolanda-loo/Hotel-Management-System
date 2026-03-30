from flask import Flask
import routes.bookings

app = Flask(__name__)

# Register the routes
app.register_blueprint(routes.bookings.booking_bp, url_prefix='/api/bookings')

if __name__ == '__main__':
    app.run(debug=True, port=5000)