from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from prometheus_flask_exporter import PrometheusMetrics

SENTIMENT_SERVICE_URL = os.environ.get('SENTIMENT_SERVICE_URL', 'http://sentiment-service:5006')

app = Flask(__name__)
metrics = PrometheusMetrics(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@postgres:5432/microservices_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    sentiment_score = db.Column(db.String(20)) # POSITIVE, NEUTRAL, NEGATIVE
    
    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "review_text": self.review_text,
            "sentiment_score": self.sentiment_score
        }

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.json
    product_id = data.get('product_id')
    user_id = data.get('user_id')
    review_text = data.get('review_text')
    
    if not all([product_id, user_id, review_text]):
        return jsonify({"message": "Invalid input"}), 400
        
    # Call Sentiment Analysis Service
    sentiment_score = "NEUTRAL"
    try:
        sentiment_response = requests.post(f"{SENTIMENT_SERVICE_URL}/analyze", json={"text": review_text}, timeout=2)
        if sentiment_response.status_code == 200:
            sentiment_score = sentiment_response.json().get('sentiment', 'NEUTRAL')
    except Exception as e:
        print(f"Error calling sentiment service: {e}")

    try:
        new_review = Review(product_id=product_id, user_id=user_id, review_text=review_text, sentiment_score=sentiment_score)
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review added", "review": new_review.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to add review: {str(e)}"}), 500

@app.route('/reviews/product/<int:product_id>', methods=['GET'])
def get_reviews_for_product(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([r.to_dict() for r in reviews]), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5005)
