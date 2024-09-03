import os
import subprocess
import re

RASPBERRYUSERNAME = "god"

def find_usb_drive():
    """
    Finds the path of the connected USB drive.
    Returns the path if found, otherwise returns None.
    """
    # This command lists all mounted drives
    result = subprocess.run(['df', '-h'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    
    # Look for a line that contains '/media/{RASPBERRYUSERNAME}/' or '/mnt/' which is typical for USB drives on Raspberry Pi
    for line in output.split('\n'):
        if f'/media/{RASPBERRYUSERNAME}/' in line or '/mnt/' in line:
            return line.split()[-1]
    return None

def open_usb_drive(usb_path):
    """
    Opens the USB drive in Finder.
    """
    subprocess.run(['open', usb_path], check=True)

def open_text_file_on_usb(usb_path, file_name):
    """
    Opens a text file on the USB drive.
    """
    file_path = os.path.join(usb_path, file_name)
    if os.path.isfile(file_path):
        subprocess.run(['open', file_path], check=True)
    else:
        print(f"File {file_name} not found on USB drive.")

def get_text_file_on_usb(usb_path, file_name):
    """
    Read context of txt file on USB drive.
    """
    file_path = os.path.join(usb_path, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        print(f"File {file_name} not found on USB drive.")
        return None

def open_image_on_usb(usb_path, file_name):
    """
    Opens an image file on the USB drive.
    """
    file_path = os.path.join(usb_path, file_name)
    if os.path.isfile(file_path):
        subprocess.run(['open', file_path], check=True)
    else:
        print(f"File {file_name} not found on USB drive.")

def find_matching_file(regex, usb_path, variable_name):
    """
    Finds a file in the USB drive directory that matches the regex pattern.
    """
    for file in os.listdir(usb_path):
        if re.match(regex, file):
            # Check if the file name (without extension) matches the variable name
            if file.startswith(variable_name):
                return file
    return 'default.png'