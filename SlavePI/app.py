import requests
import time
import socket

PORT = 2000
SUBNET = '192.168.86.'  # Update this to match your actual subnet

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