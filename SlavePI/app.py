import requests
import subprocess
import time
import socket

# URL of the localhost API
port = 2000
getinterval = 10 #in secounds
local_ip = ""
api_url = f"http://{local_ip}:{port}/master"  # Fixed string formatting for port

# Dictionary mapping variable names to file names
file_dict = {
    'var1': 'file1.png',
    'var2': 'file2.png',
    'var3': 'file3.png',
    'var4': 'file4.png',
    'var5': 'file5.png',
}

# Variable to store the last variable name
last_variable_name = None

# Function to get the local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# Get the local IP address
local_ip = get_local_ip()

while True:
    print(local_ip)
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
    
    # Wait for a short period before sending the next request
    time.sleep(getinterval)  # Wait for 5 seconds