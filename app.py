from flask import Flask
from routes.bookings import booking_bp
from routes.auth import auth_bp
from routes.housekeeping import housekeeping_bp
from routes.billing import billing_bp
from routes.reports import reports_bp
from flask import render_template

app = Flask(__name__)

# Registering all the modules we built step-by-step
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(booking_bp, url_prefix='/api/bookings')
app.register_blueprint(housekeeping_bp, url_prefix='/api/housekeeping')
app.register_blueprint(billing_bp, url_prefix='/api/billing')
app.register_blueprint(reports_bp, url_prefix='/api/reports')

@app.route('/')
def index():
    return {"status": "Hotel Management System API is Online"}, 200


#Adding the template route for dashboard
@app.route('/')
def dashboard():
    return render_template('index.html')


if __name__ == '__main__':
    # Running on port 5000
    app.run(debug=True, port=5000)