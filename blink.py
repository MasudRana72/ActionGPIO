import os
import sys
import RPi.GPIO as GPIO
from time import sleep

lock_file = "/tmp/blink.lock"
#masud
try:
    # Check if the lock file exists
    if os.path.exists(lock_file):
        # Terminate the previous instance
        with open(lock_file, 'r') as f:
            pid = int(f.read())
            os.system(f"kill {pid}")

    # Create a new lock file with the current process ID
    with open(lock_file, 'w') as f:
        f.write(str(os.getpid()))

    # Your main program logic here
    pinLED = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pinLED, GPIO.OUT)

    while True:
        GPIO.output(pinLED, GPIO.HIGH)
        print("LED on")
        sleep(0.1)
        GPIO.output(pinLED, GPIO.LOW)
        print("LED off")
        sleep(0.1)


finally:
    # Remove the lock file when the program exits (both normally and due to exceptions)
    os.remove(lock_file)
