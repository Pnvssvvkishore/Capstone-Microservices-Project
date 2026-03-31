
from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change for production

# API Gateway URL inside the Docker network
API_GATEWAY_URL = os.environ.get('API_GATEWAY_URL', 'http://api-gateway:5000')

@app.route('/health')
def health():
    return "OK", 200

@app.route('/')
def index():
    try:
        response = requests.get(f"{API_GATEWAY_URL}/products")
        if response.status_code == 200:
            products = response.json()
            for p in products:
                try:
                    rev_resp = requests.get(f"{API_GATEWAY_URL}/reviews/product/{p['id']}")
                    if rev_resp.status_code == 200:
                        p['reviews'] = rev_resp.json()
                    else:
                        p['reviews'] = []
                except:
                    p['reviews'] = []
        else:
            products = []
            flash(f"Could not fetch products: {response.text}", "error")
    except requests.exceptions.RequestException as e:
        products = []
        flash(f"Error connecting to backend: {e}", "error")
    
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            response = requests.post(f"{API_GATEWAY_URL}/register", json={
                "name": name,
                "email": email,
                "password": password
            })
            if response.status_code == 201:
                flash("Registration successful! Please login.", "success")
                return redirect(url_for('login'))
            else:
                flash(f"Registration failed: {response.text}", "error")
        except Exception as e:
            flash(f"Error: {e}", "error")
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Since the backend doesn't return a token yet (just returns success/user info), 
            # we'll implement a "mock" login session based on the successful response.
            # In a real app, we'd expect a JWT. Here we just trust the 200 OK.
            # However, the user-service /login returns user info. Let's see if we can get ID.
            
            # Re-checking user-service: It returns {"message": "Login successful", "user": ...}
            
            response = requests.post(f"{API_GATEWAY_URL}/login", json={
                "email": email,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                if 'user' in data:
                    session['user_id'] = data['user']['id']
                    session['user_name'] = data['user']['name']
                    session['user_email'] = data['user']['email']
                    flash(f"Welcome back, {session['user_name']}!", "success")
                    return redirect(url_for('index'))
                else:
                    # Fallback if user data missing
                    flash("Login successful but user data missing.", "warning")
            else:
                flash("Invalid credentials.", "error")
                
        except Exception as e:
            flash(f"Error: {e}", "error")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('index'))

@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    # Simple admin-like page to add products
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        
        try:
            payload = {
                "name": name,
                "price": float(price)
            }
            
            # Only add image_url if provided
            if image_url:
                payload["image_url"] = image_url
                
            response = requests.post(f"{API_GATEWAY_URL}/products", json=payload)
            if response.status_code == 201:
                flash("Product created successfully!", "success")
                return redirect(url_for('index'))
            else:
                flash(f"Failed: {response.text}", "error")
        except Exception as e:
            flash(f"Error: {e}", "error")
            
    return render_template('create_product.html')


@app.route('/buy/<int:product_id>', methods=['POST'])
def buy(product_id):
    if 'user_id' not in session:
        flash("Please login to buy items.", "warning")
        return redirect(url_for('login'))
        
    try:
        response = requests.post(f"{API_GATEWAY_URL}/orders", json={
            "user_id": session['user_id'],
            "product_id": product_id
        })
        if response.status_code == 201:
            flash("Order placed successfully!", "success")
        else:
            flash(f"Order failed: {response.text}", "error")
    except Exception as e:
        flash(f"Error: {e}", "error")
        
    return redirect(url_for('orders'))

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        response = requests.delete(f"{API_GATEWAY_URL}/products/{product_id}")
        if response.status_code == 200:
            flash("Product deleted successfully!", "success")
        else:
            flash(f"Failed to delete product: {response.text}", "error")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for('index'))

@app.route('/add_review/<int:product_id>', methods=['POST'])
def add_review(product_id):
    if 'user_id' not in session:
        flash("Please login to submit a review.", "warning")
        return redirect(url_for('login'))
        
    review_text = request.form.get('review_text')
    try:
        response = requests.post(f"{API_GATEWAY_URL}/reviews", json={
            "product_id": product_id,
            "user_id": session['user_id'],
            "review_text": review_text
        })
        if response.status_code == 201:
            flash("Review submitted!", "success")
        else:
            flash(f"Failed to submit review: {response.text}", "error")
    except Exception as e:
        flash(f"Error: {e}", "error")
        
    return redirect(url_for('index'))

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        response = requests.get(f"{API_GATEWAY_URL}/orders")
        if response.status_code == 200:
            all_orders = response.json()
            # Filter for current user (since backend returns all orders - simplified backend)
            user_orders = [o for o in all_orders if str(o.get('user_id')) == str(session['user_id'])]
        else:
            user_orders = []
            flash("Could not fetch orders.", "error")
    except Exception as e:
        user_orders = []
        flash(f"Error: {e}", "error")
        
    return render_template('orders.html', orders=user_orders)

@app.route('/notifications')
def notifications():
    try:
        response = requests.get(f"{API_GATEWAY_URL}/notifications")
        if response.status_code == 200:
            notes = response.json()
        else:
            notes = []
            flash("Could not fetch notifications.", "error")
    except Exception as e:
        notes = []
        flash(f"Error: {e}", "error")
        
    return render_template('notifications.html', notifications=notes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
