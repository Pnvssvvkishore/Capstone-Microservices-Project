from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
import redis
import json

app = Flask(__name__)
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@postgres:5432/microservices_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Redis Configuration
try:
    redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
except Exception as e:
    print(f"Redis connection failed: {e}")
    redis_client = None

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image_url": self.image_url
        }


@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    image_url = data.get('image_url')

    if not name or not price:
        return jsonify({"message": "Invalid input"}), 400

    try:
        new_product = Product(name=name, price=price, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"message": f"Product creation failed: {str(e)}"}), 500

    # Invalidate cache
    if redis_client:
        try:
            redis_client.delete('products_cache')
        except:
            pass

    return jsonify({"message": "Product added", "product": new_product.to_dict()}), 201


@app.route('/products', methods=['GET'])
def get_products():
    if redis_client:
        try:
            cached_products = redis_client.get('products_cache')
            if cached_products:
                return jsonify(json.loads(cached_products)), 200
        except:
            pass

    products = Product.query.all()
    products_list = [product.to_dict() for product in products]
    
    if redis_client:
        try:
            redis_client.setex('products_cache', 3600, json.dumps(products_list))
        except:
            pass
            
    return jsonify(products_list), 200


@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    if product:
        return jsonify(product.to_dict()), 200
    return jsonify({"message": "Product not found"}), 404


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    try:
        # Delete related orders first to avoid potential constraints. We wrap this in a try block 
        # because the 'orders' table may not exist yet, causing a ProgrammingError.
        try:
            db.session.execute(text("DELETE FROM orders WHERE product_id = :pid"), {"pid": id})
        except Exception:
            db.session.rollback()
            # Re-fetch product because session rollback might detach or expire the object
            product = db.session.get(Product, id)
            
        if product:
            db.session.delete(product)
            db.session.commit()
            
            # Invalidate cache
            if redis_client:
                try:
                    redis_client.delete('products_cache')
                except:
                    pass
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({"message": f"Delete failed: {str(e)}"}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002)
