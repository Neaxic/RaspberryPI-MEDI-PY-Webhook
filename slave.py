import requests
import subprocess
import time
import socket
import helpers

# URL of the localhost API
PORT = 2000
IPNET = '192.168.86.184'
ENDPOINT = 'master'
FETCHINTERVAL = 3 #in secounds
FILENAMEREGEX = r"^\d{1,6}(.png|.jpg|.jpeg)$"

# Variable to store the last variable name
last_variable_name = None
foundUSB = False
config = ""

while True:
    # Find and connect to USB drive
    if not foundUSB:
        usb_path = helpers.find_usb_drive()
    if usb_path and config == "":
        foundUSB = True
        print(f"USB drive found.", usb_path)
        # helpers.open_usb_drive(usb_path)
        # helpers.open_text_file_on_usb(usb_path, 'data.txt')
        # Open an image file on the USB drive
        # helpers.open_image_on_usb(usb_path, 'image.png')
        # Read the content of a text file on the USB drive
        config = helpers.get_text_file_on_usb(usb_path, 'config.txt')
        print(config)
    if not foundUSB and usb_path == None:
        print("USB drive not found.")
        foundUSB = False

    # Construct the API URL
    api_url = f"http://{IPNET}:{PORT}/{ENDPOINT}"
    if api_url:
        # Send a GET request to the API
        response = requests.get(api_url)
        if response.status_code == 200:
            variable_name = response.json().get('midi_message')
            if variable_name != last_variable_name:
                last_variable_name = variable_name
                file_name = helpers.find_matching_file(FILENAMEREGEX, usb_path, str(variable_name))
                print(f"Variable name: {variable_name}, File name: {file_name}")
                helpers.open_image_on_usb(usb_path, file_name)
        else:
            print("Failed to get variable name from API")
    else:
        print("Failed to connect to any IP in the list")
    
    # Wait for a short period before sending the next request
    time.sleep(FETCHINTERVAL)  # Wait for 10 seconds