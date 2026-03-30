
import subprocess

try:
    print("Building services...")
    result = subprocess.run(["docker-compose", "up", "-d", "--build", "frontend"], capture_output=True, text=True, encoding="utf-8", shell=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    if result.returncode != 0:
        print("Build failed!")
    else:
        print("Build success!")
except Exception as e:
    print("Exception:", e)
