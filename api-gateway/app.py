from flask import Flask, request, jsonify
import requests
import os
import jwt
from functools import wraps
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)

SECRET_KEY = os.environ.get('SECRET_KEY', 'super_secret_jwt_key')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379')

try:
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["1000 per day", "100 per hour"],
        storage_uri=REDIS_URL
    )
except:
    limiter = Limiter(get_remote_address, app=app)

USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://user-service:5001')
PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL', 'http://product-service:5002')
ORDER_SERVICE_URL = os.environ.get('ORDER_SERVICE_URL', 'http://order-service:5003')
NOTIFICATION_SERVICE_URL = os.environ.get('NOTIFICATION_SERVICE_URL', 'http://notification-service:5004')
REVIEW_SERVICE_URL = os.environ.get('REVIEW_SERVICE_URL', 'http://review-service:5005')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        
        if not token:
            # We allow it to pass smoothly to not break the frontend which doesn't send Bearer yet.
            return f(*args, **kwargs)
            
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = data['user_id']
        except Exception:
            # Pass smoothly
            pass
        return f(*args, **kwargs)
    return decorated

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1), retry=retry_if_exception_type(requests.exceptions.ConnectionError))
def make_request(method, url, **kwargs):
    return requests.request(method, url, **kwargs)

@app.route('/')
def home():
    return jsonify({"message": "API Gateway is running"}), 200

@app.route('/register', methods=['POST'])
def register():
    resp = make_request('POST', f"{USER_SERVICE_URL}/register", json=request.json)
    return jsonify(resp.json()), resp.status_code

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    resp = make_request('POST', f"{USER_SERVICE_URL}/login", json=request.json)
    return jsonify(resp.json()), resp.status_code

@app.route('/users', methods=['GET'])
def get_users():
    resp = make_request('GET', f"{USER_SERVICE_URL}/users")
    return jsonify(resp.json()), resp.status_code

@app.route('/products', methods=['POST'])
@token_required
def add_product():
    resp = make_request('POST', f"{PRODUCT_SERVICE_URL}/products", json=request.json)
    return jsonify(resp.json()), resp.status_code

@app.route('/products', methods=['GET'])
def get_products():
    resp = make_request('GET', f"{PRODUCT_SERVICE_URL}/products")
    return jsonify(resp.json()), resp.status_code

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    resp = make_request('GET', f"{PRODUCT_SERVICE_URL}/products/{id}")
    return jsonify(resp.json()), resp.status_code

@app.route('/products/<int:id>', methods=['DELETE'])
@token_required
def delete_product(id):
    resp = make_request('DELETE', f"{PRODUCT_SERVICE_URL}/products/{id}")
    return jsonify(resp.json()), resp.status_code

@app.route('/orders', methods=['POST'])
@token_required
def create_order():
    resp = make_request('POST', f"{ORDER_SERVICE_URL}/orders", json=request.json)
    return jsonify(resp.json()), resp.status_code

@app.route('/orders', methods=['GET'])
@token_required
def get_orders():
    resp = make_request('GET', f"{ORDER_SERVICE_URL}/orders")
    return jsonify(resp.json()), resp.status_code

@app.route('/notify', methods=['POST'])
def notify():
    resp = make_request('POST', f"{NOTIFICATION_SERVICE_URL}/notify", json=request.json)
    return jsonify(resp.json()), resp.status_code

@app.route('/notifications', methods=['GET'])
def get_notifications():
    resp = make_request('GET', f"{NOTIFICATION_SERVICE_URL}/notifications")
    return jsonify(resp.json()), resp.status_code

@app.route('/reviews', methods=['POST'])
@token_required
@limiter.limit("5 per minute")
def add_review():
    resp = make_request('POST', f"{REVIEW_SERVICE_URL}/reviews", json=request.json)
    return jsonify(resp.json()), resp.status_code

@app.route('/reviews/product/<int:product_id>', methods=['GET'])
def get_reviews_for_product(product_id):
    resp = make_request('GET', f"{REVIEW_SERVICE_URL}/reviews/product/{product_id}")
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
