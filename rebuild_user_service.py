
import subprocess
import sys

try:
    print("Starting rebuild of user-service...")
    # Build without cache to force update
    result = subprocess.run(["docker-compose", "build", "--no-cache", "user-service"], capture_output=True, text=True, encoding="utf-8", shell=True)
    with open("rebuild_user_output.txt", "w", encoding="utf-8") as f:
        f.write(result.stdout)
        f.write("\nSTDERR:\n")
        f.write(result.stderr)
    print("Build step finished with return code:", result.returncode)
    
    if result.returncode == 0:
        print("Build successful. Restarting service...")
        result_up = subprocess.run(["docker-compose", "up", "-d", "user-service"], capture_output=True, text=True, encoding="utf-8", shell=True)
        with open("restart_user_output.txt", "w", encoding="utf-8") as f:
            f.write(result_up.stdout)
            f.write("\nSTDERR:\n")
            f.write(result_up.stderr)
        print("Service restarted.")
    else:
        print("Build failed. Check rebuild_user_output.txt")
except Exception as e:
    with open("rebuild_user_error.txt", "w", encoding="utf-8") as f:
        f.write(str(e))
    print("Exception during rebuild:", e)
