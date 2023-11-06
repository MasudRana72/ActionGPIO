import tkinter as tk
from tkinter import PhotoImage

# ... (Rest of your imports and LED configuration code)
import os
import sys
import RPi.GPIO as GPIO
##Beacon GPIO 
green_beacon = 10
yellow_beacon = 9
red_beacon = 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(green_beacon, GPIO.OUT)    # green_beacon pin as output pin
GPIO.setup(yellow_beacon, GPIO.OUT)   # yellow_beacon pin as output pin
GPIO.setup(red_beacon, GPIO.OUT)      # red_beacon pin as output pin
GPIO.output(green_beacon, GPIO.LOW)   # Turn off green_beacon
GPIO.output(yellow_beacon, GPIO.LOW)  # Turn off yellow_beacon
GPIO.output(red_beacon, GPIO.LOW)     # Turn off red_beacon
#GPIO.output(18, GPIO.OUT)  # Turn off yellow_beacon
#GPIO.output(18, GPIO.LOW)     # Turn off red_beacon
from time import sleep
import time
from datetime import datetime, timedelta
import schedule
import requests
import hashlib
# URL of the forecast webpage
from ftplib import FTP
from io import BytesIO
import xml.etree.ElementTree as ET
from rpi_ws281x import PixelStrip, Color
# LED strip configuration:
LED_COUNT = 396       # Number of LED pixels.
LED_PIN = 12          # GPIO pin connected to the pixels (12 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DM A channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
brightness_Set = 255;

# Create a NeoPixel object with the appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

# Initialize the library (must be called once before other functions).
strip.begin()
print("Test beginning ✅")
import subprocess
#import sys
#sys.path.insert(0,'/home/masud/.local/lib/python3.9/site-packages')
#print(sys.path)


def check_internet_connection():
    try:
        # Ping a known website (e.g., google.com) to check for internet connectivity.
        subprocess.check_call(["ping", "-c", "1", "google.com"])
        return True
    except subprocess.CalledProcessError:
        return False

while not check_internet_connection():
    print("No internet connection. Retrying in 5 seconds...")
    time.sleep(5)

print("Internet connection established!")

digit = [
  0b000000000000001111111111111111111111111111111111111111110000000,  #0
  0b000000000000001111111000000000000000000000000000011111110000000,  #1
  0b000000000000000000000111111111111110000000111111111111111111111,  #2
  0b000000000000001111111111111100000000000000111111111111111111111,  #3
  0b000000000000001111111000000000000001111111000000011111111111111,  #4
  0b000000000000001111111111111100000001111111111111100000001111111,  #5
  0b000000000000001111111111111111111111111111111111100000001111111,  #6
  0b000000000000001111111000000000000000000000111111111111110000000,  #7
  0b000000000000001111111111111111111111111111111111111111111111111,  #8
  0b000000000000001111111111111100000001111111111111111111111111111   #9
]
#######################
# 0,50    digit group 1
# 99,148   digit group 2
# 198,247 digit group 3
# 297,346 digit group 4
#######################
##Variables
#######################
weatherzone_userid = "103173-9077"
weatherzone_password = "sap9VAgH"

Current_temp = float(0)
Forecast_temp = float(0)
uv_index_accu = float(0)
Rain_chance = float(0)
def get_bit(number, position):
    bit = (number >> position) & 1
    return bit

def send_Data(value,d1_pos,d2_pos):
    if value < 10 and value > 0:
        value_str = str(value)
        digits = value_str.split('.')
        d_1 = int(digits[0])
        d_2 = int(digits[1])
        print(d_1)
        print(d_2)
        if d_2 == 0 :
            for i in range(d1_pos,(d2_pos-1)):
                a = get_bit(digit[d_2], (i-d1_pos)) * brightness_Set
                strip.setPixelColor(i, Color(a, 0, 0))
            strip.setPixelColor(d2_pos-1, Color(0, 0, 0))
            for i in range(d2_pos,d2_pos+49):
                a = get_bit(digit[d_1], (i - d2_pos)) * brightness_Set
                strip.setPixelColor(i, Color(a, 0, 0))
            
        else:
            for i in range(d1_pos,(d2_pos-1)):
                a = get_bit(digit[d_1], (i-d1_pos)) * brightness_Set
                strip.setPixelColor(i, Color(a, 0, 0))
            strip.setPixelColor(d2_pos-1, Color(brightness_Set, 0, 0))
            for i in range(d2_pos,d2_pos+49):
                a = get_bit(digit[d_2], (i - d2_pos)) * brightness_Set
                strip.setPixelColor(i, Color(a, 0, 0))
            #strip.show()
    elif value > 0:
        value = round(value)
        d_1 = value // 10
        d_2 = value % 10
        for i in range(d1_pos,(d2_pos-1)):
            a = get_bit(digit[d_1], (i-d1_pos)) * brightness_Set
            strip.setPixelColor(i, Color(a, 0, 0))
        strip.setPixelColor(d2_pos-1, Color(0, 0, 0))
        for i in range(d2_pos,d2_pos+49):
            a = get_bit(digit[d_2], (i - d2_pos)) * brightness_Set
            strip.setPixelColor(i, Color(a, 0, 0))
        #strip.show()
    elif value <= 0:
        #value = round(value)
        d_1 = 0
        d_2 = 0
        for i in range(d1_pos,(d2_pos-1)):
            a = get_bit(digit[d_1], (i-d1_pos)) * brightness_Set
            strip.setPixelColor(i, Color(a, 0, 0))
        strip.setPixelColor(d2_pos-1, Color(0, 0, 0))
        for i in range(d2_pos,d2_pos+49):
            a = get_bit(digit[d_2], (i - d2_pos)) * brightness_Set
            strip.setPixelColor(i, Color(a, 0, 0))


def clear_buffer():
  for i in range(LED_COUNT):
    strip.setPixelColor(i, Color(0, 0, 0))
  strip.show()
  sleep(1.0)

def rgb_test():
  # print("strip.numPixels() =", strip.numPixels())
  while True:
    for i in range(396):
      # red led ✅
      strip.setPixelColor(i, Color(0, 150, 0))
      strip.show()
      sleep(0.05)
    sleep(0.1)
    


def get_data():
    global Current_temp
    global Forecast_temp
    global Rain_chance
    max_retries = 3  # Maximum number of connection retries
    retry_delay = 5  # Delay in seconds between retries
    
    for retry in range(max_retries):
        try:
            ####################################
            #
            # FTP server details
            #
            ###############################
            ftp_host = "ftp.bom.gov.au"
            ftp_dir = "/anon/gen/fwo"
            ftp_file = "IDW14104.xml"#Forecast Newman IDW14104
            ftp_file_current_temp = "IDW60920.xml"#Cureent Temperature
            # Create an FTP connection
            ftp = FTP(ftp_host)
            ftp.login()  # For anonymous access

            # Change to the appropriate directory on the FTP server
            ftp.cwd(ftp_dir)

            # Initialize a BytesIO object to store the file's contents in-memory
            file_data = BytesIO()
            file_data_ct = BytesIO()

            # Retrieve the file and store its contents in the BytesIO object
            ftp.retrbinary("RETR " + ftp_file, file_data.write)
            ftp.retrbinary("RETR " + ftp_file_current_temp, file_data_ct.write)

            # Rewind the BytesIO object to the beginning of the data
            file_data.seek(0)
            file_data_ct.seek(0)

            # Close the FTP connection
            ftp.quit()

            # Now you can process the data in-memory
            file_contents = file_data.read().decode("utf-8")
            file_contents_ct = file_data_ct.read().decode("utf-8")

            # Parse the XML data
            root = ET.fromstring(file_contents)
            root_ct = ET.fromstring(file_contents_ct)

            # Find the forecast-period for location
            perth_forecast_period = root.find(".//area[@aac='WA_PT014']")#perth location code.
            perth_ct = root_ct.find(".//station[@wmo-id='99312']")#COONDEWANNA location code.#Cureent Temperature

            # Extract the 'probability_of_precipitation' and 'air_temperature_maximum' values
            try:
                probability_of_precipitation = perth_forecast_period.find(".//text[@type='probability_of_precipitation']").text
        
            except AttributeError:
                probability_of_precipitation = "N/A"

            try:
                air_temperature_maximum = perth_forecast_period.find(".//element[@type='air_temperature_maximum']").text
            except AttributeError:
                air_temperature_maximum = "N/A"
            try:
               current_temp = perth_ct.find(".//element[@type='air_temperature']").text
            except AttributeError:
                current_temp = "N/A"
            break
        except socket.gaierror as e:
            if retry < max_retries - 1:
                print(f"FTP connection failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Max retries reached. Unable to connect.")
                log_entry(f"FTP connection failed after {max_retries} retries: {e}")
                # Continue with the rest of the program
                break  # Exit the loop without re-raising the exception

    # Print the extracted values
    
    Current_temp = float(current_temp)
    print("Cureent Air Temperature:", current_temp)
    Forecast_temp= float(air_temperature_maximum)
    print("Probability of Precipitation:", probability_of_precipitation)
    Rain_chance = float(probability_of_precipitation.rstrip('%'))
    print("Air Temperature Maximum:", air_temperature_maximum)
    Forecast_temp= float(air_temperature_maximum)
def weatherzone_data():
    #####
    ##LIGHTNING DATA FETCHING FROM WEATHERZONE.COM
    #######
    url_weatherzone = "https://ws.weatherzone.com.au/?lt=uwas&lc=1586&locdet=1&latlon=1&alerts=1(client=1471,type=lightning)&format=xml"
    def generate_key(weatherzone_password):
        key = None
        today = datetime.now().strftime("%d/%m/%y")

        if today:
            day, month, year = map(int, today.split('/'))
            #print(day)
            key = str(day * 2 + month * 100 * 3 + year * 10000 * 17) + str(weatherzone_password)
            #print(key)
            m = hashlib.md5()
            m.update(key.encode('utf-8'))
            i = int.from_bytes(m.digest(), byteorder='big')
            generated_key = f"{i:032X}".lower()
            return generated_key

        return key
    generated_key = generate_key(weatherzone_password)
    #print(generated_key)
    url_weatherzone = url_weatherzone +"&u=" + weatherzone_userid + "&k=" +generated_key
    response = requests.get(url_weatherzone)
    if response.status_code == 200:
        weatherzone_data = response.text
        #print(weatherzone_data)

        # Parse the XML data
        root = ET.fromstring(weatherzone_data)

        # Iterate through alert elements to find the one with status="CLEAR"
        for alert_element in root.iter("alert"):
            status_value = alert_element.get("status")
            if status_value == "CLEAR":
                GPIO.output(yellow_beacon, GPIO.LOW)  # Turn off yellow_beacon
                GPIO.output(red_beacon, GPIO.LOW)     # Turn off red_beacon
                GPIO.output(green_beacon, GPIO.HIGH)   # Turn ON green_beacon
                print(f"Status attribute value: {status_value}")
                break  # Stop searching once a "CLEAR" status is found
            elif status_value == "APPROACHING":
                GPIO.output(green_beacon, GPIO.LOW)   # Turn off green_beacon
                GPIO.output(red_beacon, GPIO.LOW)     # Turn off red_beacon
                GPIO.output(yellow_beacon, GPIO.HIGH)  # Turn ON yellow_beacon
                print(f"Status attribute value: {status_value}")
                break  # Stop searching once a "CLEAR" status is found
            elif status_value == "IMMINENT":
                GPIO.output(green_beacon, GPIO.LOW)   # Turn off green_beacon
                GPIO.output(yellow_beacon, GPIO.LOW)  # Turn off yellow_beacon
                GPIO.output(red_beacon, GPIO.HIGH)     # Turn ON red_beacon
                print(f"Status attribute value: {status_value}")
                break  # Stop searching once a "CLEAR" status is found
            else:
                print("No alert with status=\"CLEAR\" found in the XML.")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

###########
# Fetching UV index data from accuweather api, an free api provided by accuweather, can ping it 50times a day.
###########
def fetch_uv_index():
    # Replace 'YOUR_API_KEY' with your actual AccuWeather API key
    api_key = 'dhWLws0grWpP3XnFJDIqyPIAEA0H3QlE'  # 50 free calls per day

    # AccuWeather API endpoint for current conditions
    location_key = 16731  # Replace with your desired location key
    endpoint = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}'

    # Parameters for the request
    params = {
        'apikey': api_key,
        'details': 'true',  # Include details such as UV index
    }

    try:
        # Send a GET request to AccuWeather API
        response = requests.get(endpoint, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Extract UV index data
            if data and isinstance(data, list) and 'UVIndex' in data[0]:
                uv_index = data[0]['UVIndex']
                return float(uv_index)
            else:
                print('UV Index data not found in the response.')
        else:
            print(f'Error: Unable to retrieve data. Status Code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

    return None  # Return None in case of errors

def update_uv_index():
    global uv_index_accu

    # Get the current time
    current_time = datetime.now().time()

    # Check if the current time is within the allowed time range (5:30 AM to 7 PM)
    if current_time >= datetime.strptime('05:30:00', '%H:%M:%S').time() and current_time <= datetime.strptime('19:00:00', '%H:%M:%S').time():
        uv_index = fetch_uv_index()
        if uv_index is not None:
            uv_index_accu = uv_index
            print(f'UV Index: {uv_index_accu}')
        else:
            print('UV Index update failed.')
    else:
        print('UV Index update time up.')
def main():
    schedule.every(20).minutes.do(update_uv_index)  # Schedule the API call every 20 minutes

#LOOP FUNCTION 

weatherstation_lock_file = "/tmp/weatherstation.lock"
# Specify the path to your log file
log_file_path = "/home/rubixdesign/actions-runner/_work/ActionGPIO/ActionGPIO/log.txt"

def log_entry(text_to_write):
    with open(log_file_path, "a") as log_file:
        # Write the text to the file
        log_file.write(text_to_write)
    log_file.close()

# Check if the lock file exists
if os.path.exists(weatherstation_lock_file):
    # Terminate the previous instance
    with open(weatherstation_lock_file, 'r') as f:
        pid = int(f.read())
        os.system(f"kill {pid}")

weatherstation_lock_file = "/tmp/weatherstation.lock"
# Create a new lock file with the current process ID
with open(weatherstation_lock_file, 'w') as f:
    f.write(str(os.getpid()))
    
# Create a function to update the weather data and LEDs
def update_weather_and_leds():
    #get_data()
    #update_uv_index()
    weatherzone_data()

    # Assuming you have the values in Current_temp, Forecast_temp, uv_index_accu, and Rain_chance

    # Format the values based on your criteria
    Current_temp = 38.55
    Forecast_temp = 33.45
    Rain_chance = 5.0
    uv_index_accu =7.8
    current_temp_text = "{:.1f}".format(Current_temp) if Current_temp < 10 else "{:.0f}".format(Current_temp)
    forecast_temp_text = "{:.1f}".format(Forecast_temp) if Forecast_temp < 10 else "{:.0f}".format(Forecast_temp)
    uv_index_text = "{:.1f}".format(uv_index_accu) if uv_index_accu < 10 else "{:.0f}".format(uv_index_accu)
    rain_chance_text = "{:.1f}".format(Rain_chance) if Rain_chance < 10 else "{:.0f}".format(Rain_chance)
    canvas.create_rectangle(50, 50, 80, 80, fill="gray")

    # Update labels with the new values
    labels[0].config(text=current_temp_text)
    labels[1].config(text=forecast_temp_text)
    labels[2].config(text=uv_index_text)
    labels[3].config(text=rain_chance_text)


    # Update LED display based on the new values
    send_Data(Current_temp,  0, 50)  # Update digit group 1
    send_Data(Forecast_temp, 99, 149)  # Update digit group 2
    send_Data(uv_index_accu, 198, 248)  # Update digit group 3
    send_Data(Rain_chance, 297, 347)  # Update digit group 4
    strip.show()
    # Schedule the next update in 5 minutes
    window.after(300000, update_weather_and_leds)


# Create a Tkinter window
window = tk.Tk()
window.title("SMART WEATHER WARNING STATION")

# Load the background image
bg_image = PhotoImage(file="/home/masud/weatherboard.png")
image_width = bg_image.width()
image_height = bg_image.height()

# Create a canvas to display the background image
canvas = tk.Canvas(window, width=image_width, height=image_height)
canvas.pack()

# Display the background image
canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

# Create labels with the formatted variables
labels = [
    tk.Label(window, text="", font=("Digital-7", 60), fg="red", bg="white"),
    tk.Label(window, text="", font=("Digital-7", 60), fg="red", bg="white"),
    tk.Label(window, text="", font=("Digital-7", 60), fg="red", bg="white"),
    tk.Label(window, text="", font=("Digital-7", 60), fg="red", bg="white"),
]

# Calculate label positions
text_positions = [
    (((image_width / 4 - len(labels[0]['text']) * 10) / 2) , (image_height / 4) * 3),
    ((image_width / 4 * 3 - len(labels[1]['text']) * 10) / 2, (image_height / 4) * 3),
    ((image_width / 4 * 5 - len(labels[2]['text']) * 10) / 2, (image_height / 4) * 3),
    ((image_width / 4 * 7 - len(labels[3]['text']) * 10) / 2, (image_height / 4) * 3),
]

# Place the labels in their respective positions
for label, (x, y) in zip(labels, text_positions):
    label.place(x=x, y=y)


# Disable window resizing
window.resizable(False, False)

# Call the update function to initialize the data and LEDs
update_weather_and_leds()

# Start the GUI main loop
window.mainloop()
