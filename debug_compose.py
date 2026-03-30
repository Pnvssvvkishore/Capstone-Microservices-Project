
import subprocess

try:
    print("Running docker-compose up...")
    res = subprocess.run(["docker-compose", "up", "-d"], capture_output=True, text=True, encoding="utf-8", shell=True)
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
except Exception as e:
    print("Exception running docker-compose:", e)
