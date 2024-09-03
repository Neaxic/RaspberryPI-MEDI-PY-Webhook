import requests
import subprocess
import time
import socket

# URL of the localhost API
PORT = 2000
SUBNET = '192.168.1.'
getinterval = 10 #in secounds
api_endpoint = "master"  # Fixed string formatting for port

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

def find_master():
    for i in range(1, 255):  # Scan all possible IP addresses in the subnet
        ip = f"{SUBNET}{i}"
        try:
            with socket.create_connection((ip, PORT), timeout=0.1):
                return ip
        except (socket.timeout, ConnectionRefusedError):
            continue
    return None

def get_midi_data():
    master_ip = find_master()
    if master_ip:
        try:
            response = requests.get(f"http://{master_ip}:{PORT}/master")
            if response.status_code == 200:
                return response.json()['midi_message']
            else:
                print(f"Error: Received status code {response.status_code}")
        except requests.RequestException as e:
            print(f"Error connecting to master: {e}")
    else:
        print("Master not found")
    return None

while True:
    midi_data = get_midi_data()
    if midi_data:
        print(f"Received MIDI data: {midi_data}")
    time.sleep(1)  # Wait for 1 second before next request