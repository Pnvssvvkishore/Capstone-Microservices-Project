
import subprocess
import requests
import time

# Restart service
with open("final_output.txt", "w", encoding="utf-8") as f:
    f.write("Restarting notification-service...\n")
    subprocess.run(["docker-compose", "up", "-d", "notification-service"], check=True)

    f.write("Waiting for service to be ready...\n")
    for i in range(10):
        try:
            resp = requests.get("http://localhost:5004/notifications")
            f.write(f"Response status: {resp.status_code}\n")
            f.write("Response body:\n")
            f.write(resp.text)
            break
        except Exception as e:
            f.write(f"Attempt {i+1} failed: {e}\n")
            time.sleep(2)

