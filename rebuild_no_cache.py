
import subprocess
import sys

try:
    result = subprocess.run(["docker-compose", "build", "--no-cache", "notification-service"], capture_output=True, text=True, encoding="utf-8", shell=True)
    with open("rebuild_output.txt", "w", encoding="utf-8") as f:
        f.write(result.stdout)
        f.write("\nSTDERR:\n")
        f.write(result.stderr)
    print("Build step finished with return code:", result.returncode)
except Exception as e:
    with open("rebuild_output.txt", "w", encoding="utf-8") as f:
        f.write(str(e))
    print("Exception during rebuild:", e)
