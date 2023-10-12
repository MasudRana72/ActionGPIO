import subprocess

script_path = "/home/masud/actions-runner/_work/ActionGPIO/ActionGPIO/blink.py"

try:
    process = subprocess.Popen(["python3", script_path], check=True, cwd="/home/masud/actions-runner/_work/ActionGPIO/ActionGPIO")
except subprocess.CalledProcessError as e:
    print(f"Error running the script: {e}")
