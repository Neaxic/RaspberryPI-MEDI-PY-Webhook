import requests
import subprocess
import time

# URL of the localhost API
port = 5000
getinterval = 5 #in secounds
api_url = f"http://localhost:{port}/master"  # Fixed string formatting for port

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

while True:
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