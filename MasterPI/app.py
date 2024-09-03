import midi
import os
import subprocess
from flask import Flask, request, abort, jsonify
import threading
import socket

app = Flask(__name__)

# MIDI connection settings
conn = midi.MidiConnector('/dev/serial0', baudrate=38400, timeout=1)
note = 70
channel = 0
msg = None  # This will be overwritten by read()
PORT = 2000
password = "asdl"  # maybe not even have one

cc = 0
pc = 0

# Create a lock for synchronizing access to the msg variable
msg_lock = threading.Lock()

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Dynamically get the IP address
IP_ADDRESS = get_ip_address()
print(f"Server IP: {IP_ADDRESS}")

@app.route('/master', methods=['GET'])
def webhook():
    if request.method == 'GET':
        with msg_lock:
            # Ensure a valid response is returned
            if msg is None:
                return jsonify({"status": "No MIDI data available"}), 204  # 204 No Content
            else:
                return jsonify({"midi_message": msg}), 200
    else:
        abort(400)

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

def midi_listener():
    global msg, cc, pc
    while True:
        try:
            raw_data = conn.read()
            if raw_data is not None:
                print("---------------------------------new msg------------------------")
                if "ProgramChange" in str(raw_data.type):
                    pc = raw_data.program_number
                if "ControlChange" in str(raw_data.type):
                    cc = raw_data.value
                
                # Process the raw MIDI data
                num = cc * 128 + pc + 1

                with msg_lock:
                    msg = num  # Assign the processed message
                print(f"-> END -- Processed MIDI Message: {msg} - cc {cc} - pc {pc}")
        except AssertionError as e:
            print(f"AssertionError: {e}")
        except TypeError:
            print("MIDI read error")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == '__main__':
    # Start the Flask API server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Allows Flask thread to exit when the main program exits
    flask_thread.start()

    # Start listening to MIDI signals in the main thread
    midi_listener()