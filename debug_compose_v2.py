
import subprocess

with open("compose_error.txt", "w", encoding="utf-8") as f:
    try:
        f.write("Running docker-compose up...\n")
        res = subprocess.run(["docker-compose", "up", "-d"], capture_output=True, text=True, encoding="utf-8", shell=True)
        f.write("STDOUT:\n" + res.stdout + "\n")
        f.write("STDERR:\n" + res.stderr + "\n")
        f.write(f"Return Code: {res.returncode}\n")
    except Exception as e:
        f.write(f"Exception: {e}\n")
