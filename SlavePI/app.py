import requests
import subprocess
import time
import socket
import helpers

# URL of the localhost API
PORT = 2000
IPNET = '192.168.86.184'
ENDPOINT = 'master'
FETCHINTERVAL = 1 #in secounds
USBNAME = "NONAME"

# Variable to store the last variable name
last_variable_name = None

# Dictionary mapping variable names to file names
file_dict = {
    'var1': 'file1.png',
    'var2': 'file2.png',
    'var3': 'file3.png',
    'var4': 'file4.png',
    'var5': 'file5.png',
}

while True:
    # Find and connect to USB drive
    usb_path = helpers.find_usb_drive()
    if usb_path:
        print(f"USB drive found.", usb_path)
        # Open the USB drive in Finder
        helpers.open_usb_drive(usb_path)
        # Open a text file on the USB drive
        helpers.open_text_file_on_usb(usb_path, 'data.txt')
        # Open an image file on the USB drive
        helpers.open_image_on_usb(usb_path, 'image.png')
    else:
        print("USB drive not found.")
    # Construct the API URL
    api_url = f"http://{IPNET}:{PORT}/{ENDPOINT}"
    if api_url:
        # Send a GET request to the API
        response = requests.get(api_url)
        if response.status_code == 200:
            # Extract the variable name from the response
            variable_name = response.json().get('variable_name')
            # Check if the variable name has changed
            if variable_name != last_variable_name:
                # Update the last variable name
                last_variable_name = variable_name
                # Get the file name based on the variable name, default to 'default.png'
                file_name = file_dict.get(variable_name, 'default.png')
                # Open the file
                subprocess.run(['open', file_name], check=True)
        else:
            print("Failed to get variable name from API")
    else:
        print("Failed to connect to any IP in the list")
    
    # Wait for a short period before sending the next request
    time.sleep(FETCHINTERVAL)  # Wait for 10 seconds