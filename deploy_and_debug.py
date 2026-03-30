
import subprocess
import requests
import time
import sys

def log(msg):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

# Clear log
open("debug_log.txt", "w").close()

log("Starting deployment of notification-service...")

try:
    # Up
    res = subprocess.run(["docker-compose", "up", "-d", "notification-service"], capture_output=True, text=True, encoding="utf-8")
    log(f"Up stdout: {res.stdout}")
    log(f"Up stderr: {res.stderr}")
    if res.returncode != 0:
        log("Failed to start service")
        sys.exit(1)

    log("Waiting for service...")
    time.sleep(5)

    # Test
    log("Testing GET /notifications...")
    try:
        resp = requests.get("http://localhost:5004/notifications")
        log(f"Status: {resp.status_code}")
        log(f"Body: {resp.text}")
    except Exception as e:
        log(f"Request failed: {e}")

except Exception as e:
    log(f"Script failed: {e}")
