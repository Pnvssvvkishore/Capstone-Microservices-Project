import requests
import time
import sys
import json

BASE_URL = "http://localhost:5000"

def log(msg, status="INFO"):
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }
    print(f"{colors.get(status, '')}[{status}] {msg}{colors['RESET']}")

def check_endpoint(method, endpoint, payload=None, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == expected_status:
            log(f"{method} {endpoint} - Success ({response.status_code})", "SUCCESS")
            return response.json() if response.content else {}
        else:
            log(f"{method} {endpoint} - Failed (Expected {expected_status}, Got {response.status_code})", "ERROR")
            log(f"Response: {response.text}", "ERROR")
            return None
    except Exception as e:
        log(f"{method} {endpoint} - Exception: {e}", "ERROR")
        return None

def verify_all():
    log("Starting comprehensive verification...");
    
    # Wait for API Gateway to be ready
    log("Waiting for API Gateway to be ready...")
    for i in range(10):
        try:
            resp = requests.get(BASE_URL, timeout=5)
            if resp.status_code == 200:
                log("API Gateway is ready!", "SUCCESS")
                break
        except:
            pass
        log(f"Waiting for services... ({i+1}/10)", "INFO")
        time.sleep(2)
    else:
        log("API Gateway timed out or not rechable", "ERROR")
        return
    
    # 1. Register User
    user_payload = {"name": "Test User", "email": f"test_{int(time.time())}@example.com", "password": "password123"}
    log("1. Testing User Registration...")
    reg_resp = check_endpoint("POST", "/register", user_payload, 201)
    if not reg_resp: return

    # 2. Login User
    log("2. Testing User Login...")
    login_payload = {"email": user_payload["email"], "password": user_payload["password"]}
    check_endpoint("POST", "/login", login_payload, 200)

    # 3. Add Product
    log("3. Testing Product Creation...")
    product_payload = {"name": "Test Product", "price": 100.0}
    prod_resp = check_endpoint("POST", "/products", product_payload, 201)
    if not prod_resp: return
    product_id = prod_resp.get("product", {}).get("id")

    # 4. Create Order
    log("4. Testing Order Creation...")
    # We need the user ID from registration or just assume 1 if it's the first run, 
    # but the registration response returns the user object.
    user_id = reg_resp.get("user", {}).get("id")
    if not user_id or not product_id:
        log("Cannot proceed with Order test (missing IDs)", "ERROR")
        return

    order_payload = {"user_id": user_id, "product_id": product_id}
    check_endpoint("POST", "/orders", order_payload, 201)

    # 5. Check Notifications
    log("5. Testing Notifications Log...")
    # Give it a moment for the async/sync call to propagate if needed
    time.sleep(1) 
    check_endpoint("GET", "/notifications", expected_status=200)

    # 6. Check Metrics
    log("6. Testing Prometheus Metrics Exposure...")
    try:
        metrics_resp = requests.get("http://localhost:5000/metrics")
        if metrics_resp.status_code == 200:
             log("API Gateway Metrics Exposed", "SUCCESS")
        else:
             log("API Gateway Metrics Failed", "ERROR")
    except:
        log("Could not connect to API Gateway metrics", "ERROR")

    log("Verification Complete!", "SUCCESS")

if __name__ == "__main__":
    verify_all()
