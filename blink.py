import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pinout = 18
color = "Yellow"
GPIO.setup(pinout,GPIO.OUT)
print "LED on N" + str(pinout) + " " + color
GPIO.output(pinout,GPIO.HIGH)
time.sleep(1)
print "LED off N" + str(pinout) + " " + color
GPIO.output(pinout,GPIO.LOW)
time.sleep(1)
