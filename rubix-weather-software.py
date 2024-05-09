import requests
import xml.etree.ElementTree as ET

url_weatherzone = "https://ws.weatherzone.com.au/?lt=uwas&lc=7027&locdet=1&latlon=1&alerts=1(client=393,type=lightning)&format=xml"
import hashlib
from datetime import datetime

def generate_key(weatherzone_password):
    key = None
    today = datetime.now().strftime("%d/%m/%y")

    if today:
        day, month, year = map(int, today.split('/'))
        key = str(day * 2 + month * 100 * 3 + year * 10000 * 17) + str(weatherzone_password)
        print(day)
        print(key)
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        i = int.from_bytes(m.digest(), byteorder='big')
        generated_key = f"{i:032X}".lower()
        return generated_key

    return key

weatherzone_userid = "103173-9077"
weatherzone_password = "sap9VAgH"
generated_key = generate_key(weatherzone_password)
print(generated_key)
url_weatherzone = url_weatherzone +"&u=" + weatherzone_userid + "&k=" +generated_key
#print(url_weatherzone)
try:
    response = requests.get(url_weatherzone)

    if response.status_code == 200:
        print("Success")
        xml_data = response.text
        print(xml_data)

        # Parse the XML data
        root = ET.fromstring(xml_data)

        # Iterate through alert elements to find the one with status="CLEAR"
        for alert_element in root.iter("alert"):
            status_value = alert_element.get("status")
            print(f"Status attribute value: {status_value}")
            if status_value == "CLEAR":
                print(f"Status attribute value: {status_value}")
                break  # Stop searching once a "CLEAR" status is found

            else:
                
                print("No alert with status=\"CLEAR\" found in the XML.")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
