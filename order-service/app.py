from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import pika
import json

app = Flask(__name__)
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@postgres:5432/microservices_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "product_id": self.product_id}

PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL', 'http://product-service:5002')
NOTIFICATION_SERVICE_URL = os.environ.get('NOTIFICATION_SERVICE_URL', 'http://notification-service:5004')
RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')

    if not user_id or not product_id:
        return jsonify({"message": "Invalid input"}), 400

    # Verify product exists
    try:
        # Fetch specific product to check existence
        resp = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
        if resp.status_code == 200:
            # Product exists
            pass 
        elif resp.status_code == 404:
            return jsonify({"message": "Product not found"}), 404
        else:
             return jsonify({"message": "Failed to validate product"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Error connecting to Product Service: {str(e)}"}), 503

    # Create Order
    new_order = Order(user_id=user_id, product_id=product_id)
    db.session.add(new_order)
    db.session.commit()

    # Publish to RabbitMQ for async notification delivery
    try:
        params = pika.URLParameters(RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='notifications')
        
        payload = {"user": str(user_id), "message": f"Order placed for product {product_id}"}
        channel.basic_publish(exchange='', routing_key='notifications', body=json.dumps(payload))
        connection.close()
    except Exception as e:
        print(f"Failed to send notification via RabbitMQ: {e}")

    return jsonify({"message": "Order created", "order": new_order.to_dict()}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders]), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5003)
