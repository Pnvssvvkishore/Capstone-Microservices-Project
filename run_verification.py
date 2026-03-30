
import subprocess

try:
    with open("verify_result.txt", "w", encoding="utf-8") as f:
        subprocess.run(["python", "verify_deployment.py"], stdout=f, stderr=subprocess.STDOUT, check=True)
    print("Verification passed!")
except subprocess.CalledProcessError as e:
    print("Verification failed!")
except Exception as e:
    print(f"Error: {e}")
