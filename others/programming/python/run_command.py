proc = subprocess.Popen(["infinite_app", "param"], shell=True)
try:
    proc.wait(timeout=3)
except subprocess.TimeoutExpired:
    kill(proc.pid)
