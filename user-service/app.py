from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
# Database connection: user:password@hostname:port/db_name
# We will use the main postgres container.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@postgres:5432/microservices_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super_secret_jwt_key')

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"message": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
       return jsonify({"message": "User already exists"}), 400

    try:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"message": f"Registration failed: {str(e)}"}), 500
    
    # Notify Notification Service
    try:
        notification_service = os.environ.get('NOTIFICATION_SERVICE_URL', 'http://notification-service:5004')
        import requests
        requests.post(f"{notification_service}/notify", json={
            "user": email, # Send email as user identifier for notification
            "message": f"Welcome {name}!"
        }, timeout=1) 
    except Exception as e:
        print(f"Failed to send notification: {e}")

    return jsonify({"message": "User registered successfully", "user": new_user.to_dict()}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"message": "Login successful", "token": token, "user": user.to_dict()}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

if __name__ == '__main__':
    # Create tables if they don't exist (Useful for dev, but init.sql is better for prod)
    # We'll rely on init.sql or manual creation, but this helps auto-create if DB is empty.
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001)
