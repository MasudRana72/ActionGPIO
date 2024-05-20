import requests
import xml.etree.ElementTree as ET
import hashlib
from datetime import datetime
import os
import RPi.GPIO as GPIO
import time

# Suppress GPIO warnings
GPIO.setwarnings(False)

# Beacon GPIO pins
green_beacon = 10
yellow_beacon = 9
red_beacon = 11
R1_beacon = 23
R2_beacon = 24
R3_beacon = 17

# Set up GPIO
GPIO.setmode(GPIO.BCM)
beacons = [green_beacon, yellow_beacon, red_beacon, R1_beacon, R2_beacon, R3_beacon]
for beacon in beacons:
    GPIO.setup(beacon, GPIO.OUT)
    GPIO.output(beacon, GPIO.LOW)  # Turn off all beacons initially

weatherzone_userid = "103173-9077"
weatherzone_password = "sap9VAgH"

def generate_key(weatherzone_password):
    today = datetime.now().strftime("%d/%m/%y")
    day, month, year = map(int, today.split('/'))
    key = f"{day * 2 + month * 100 * 3 + year * 10000 * 17}{weatherzone_password}"
    m = hashlib.md5()
    m.update(key.encode('utf-8'))
    return f"{int.from_bytes(m.digest(), byteorder='big'):032X}".lower()

def check_internet_connection(url='http://www.google.com/', timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        return True if response.status_code == 200 else False
    except requests.ConnectionError:
        return False

def weatherzone_data():
    url_weatherzone = "https://ws.weatherzone.com.au/?lt=uwas&lc=7027&locdet=1&latlon=1&alerts=1(client=393,type=lightning)&format=xml"
    generated_key = generate_key(weatherzone_password)
    url_weatherzone = f"{url_weatherzone}&u={weatherzone_userid}&k={generated_key}"
    
    try:
        response = requests.get(url_weatherzone)
        response.raise_for_status()
        weatherzone_data = response.text
        root = ET.fromstring(weatherzone_data)

        for alert_element in root.iter("alert"):
            status_value = alert_element.get("status")
            if status_value == "CLEAR":
                GPIO.output(R1_beacon, GPIO.LOW)
                GPIO.output(yellow_beacon, GPIO.LOW)
                GPIO.output(red_beacon, GPIO.LOW)
                GPIO.output(green_beacon, GPIO.HIGH)
                break
            elif status_value == "BRAVO":
                GPIO.output(R1_beacon, GPIO.LOW)
                GPIO.output(green_beacon, GPIO.LOW)
                GPIO.output(red_beacon, GPIO.LOW)
                GPIO.output(yellow_beacon, GPIO.HIGH)
                break
            elif status_value == "CHARLIE":
                GPIO.output(R1_beacon, GPIO.LOW)
                GPIO.output(green_beacon, GPIO.LOW)
                GPIO.output(yellow_beacon, GPIO.LOW)
                GPIO.output(red_beacon, GPIO.HIGH)
                break
            elif status_value == "ALPHA":
                GPIO.output(R1_beacon, GPIO.HIGH)
                GPIO.output(green_beacon, GPIO.LOW)
                GPIO.output(yellow_beacon, GPIO.LOW)
                GPIO.output(red_beacon, GPIO.LOW)
                break
            else:
                print(f"Unexpected status: {status_value}")

    except requests.RequestException as e:
        print(f"Failed to retrieve data: {e}")
        turn_off_all_beacons()

def turn_off_all_beacons():
    for beacon in beacons:
        GPIO.output(beacon, GPIO.LOW)


while True:
    if check_internet_connection():
        print("Internet connection established!")
        weatherzone_data()
    else:
        print("No internet connection. Turning off all beacons.")
        turn_off_all_beacons()

    time.sleep(1)
