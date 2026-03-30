from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import pika
import json
import threading
import time

app = Flask(__name__)
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@postgres:5432/microservices_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False) # "user" in prompt, usage implies email or id
    message = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {"id": self.id, "user": self.user_id, "message": self.message}

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    user = data.get('user')
    message = data.get('message')

    if not user or not message:
        return jsonify({"message": "Invalid input"}), 400

    new_notification = Notification(user_id=user, message=message)
    db.session.add(new_notification)
    db.session.commit()

    # Simulate sending email/SMS
    print(f"SENDING NOTIFICATION TO {user}: {message}")

    return jsonify({"message": "Notification sent", "notification": new_notification.to_dict()}), 201

@app.route('/notifications', methods=['GET'])
def get_notifications():
    try:
        notifications = Notification.query.all()
        return jsonify([n.to_dict() for n in notifications]), 200
    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    def listen_for_notifications():
        while True:
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
                channel = connection.channel()
                channel.queue_declare(queue='notifications')

                def callback(ch, method, properties, body):
                    data = json.loads(body)
                    user = data.get('user')
                    message = data.get('message')
                    with app.app_context():
                        new_notification = Notification(user_id=user, message=message)
                        db.session.add(new_notification)
                        db.session.commit()
                        print(f"RABBITMQ RECEIVED: SENDING NOTIFICATION TO {user}: {message}")

                channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)
                print("Started consuming RabbitMQ 'notifications' queue")
                channel.start_consuming()
            except Exception as e:
                print(f"RabbitMQ consumer error: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    # Start consumer thread
    threading.Thread(target=listen_for_notifications, daemon=True).start()

    app.run(host='0.0.0.0', port=5004)
