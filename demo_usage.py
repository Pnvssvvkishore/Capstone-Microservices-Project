
import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"

def print_json(data, label="Response"):
    print(f"\n--- {label} ---")
    print(json.dumps(data, indent=2))
    print("----------------\n")

def run_demo():
    print("=== Microservices Usage Demo ===")
    print("This script simulates a real user flow to show you the output of each service.\n")

    # Step 1: Register User
    print("Step 1: Registering a new user...")
    email = f"user_{int(time.time())}@example.com"
    payload = {
        "name": "Demo User", 
        "email": email, 
        "password": "password123"
    }
    print(f"Sending POST /register with: {json.dumps(payload)}")
    resp = requests.post(f"{BASE_URL}/register", json=payload)
    if resp.status_code == 201:
        data = resp.json()
        print_json(data, "Created User")
        user_id = data.get("user", {}).get("id")
    else:
        print(f"Failed: {resp.status_code} - {resp.text}")
        return

    # Step 2: Create Product
    print("Step 2: Creating a new product...")
    payload = {
        "name": "Super fast Laptop", 
        "price": 1200.50
    }
    print(f"Sending POST /products with: {json.dumps(payload)}")
    resp = requests.post(f"{BASE_URL}/products", json=payload)
    if resp.status_code == 201:
        data = resp.json()
        print_json(data, "Created Product")
        product_id = data.get("product", {}).get("id")
    else:
        print(f"Failed: {resp.status_code} - {resp.text}")
        return

    # Step 3: Place Order
    print("Step 3: Placing an order for the new product...")
    payload = {
        "user_id": user_id, 
        "product_id": product_id
    }
    print(f"Sending POST /orders with: {json.dumps(payload)}")
    resp = requests.post(f"{BASE_URL}/orders", json=payload)
    if resp.status_code == 201:
        data = resp.json()
        print_json(data, "Order Confirmation")
    else:
        print(f"Failed: {resp.status_code} - {resp.text}")
        return

    # Step 4: Check Notifications
    print("Step 4: Checking notifications (triggered by Order Service)...")
    time.sleep(1) # Wait for async processing if any
    resp = requests.get(f"{BASE_URL}/notifications")
    if resp.status_code == 200:
        data = resp.json()
        print_json(data, "Notification Log")
        print("Note: You should see a notification above corresponding to the order you just placed.")
    else:
        print(f"Failed: {resp.status_code} - {resp.text}")

    print("\n=== Demo Complete ===")
    print("To see the internal logs of these actions, look at your 'docker-compose logs' terminal.")

if __name__ == "__main__":
    try:
        run_demo()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API Gateway at http://localhost:5000")
        print("Make sure your Docker containers are running (docker-compose up --build).")
