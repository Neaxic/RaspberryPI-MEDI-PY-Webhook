import midi
import os
import subprocess
from flask import Flask, request, abort, jsonify
import threading

app = Flask(__name__)

# MIDI connection settings
conn = midi.MidiConnector('/dev/serial0', baudrate=38400, timeout=1)
note = 70
channel = 0
msg = None  # This will be overwritten by read()
port = 2000
password = "asdl"  # maybe not even have one

@app.route('/master', methods=['GET'])
def webhook():
    # Uncomment the following lines if you need password protection
    # query_password = request.args.get('password', '')  # Defaults to empty string if not found
    # if query_password != password:
    #     return "Unauthorized", 401  # Unauthorized access

    if request.method == 'GET':
        # Ensure a valid response is returned
        if msg is None:
            return jsonify({"status": "No MIDI data available"}), 204  # 204 No Content
        else:
            # Convert the MIDI message to a JSON-serializable format
            midi_data = {
                "status": msg.status,  # Replace with the actual property names
                "data1": msg.data1,    # Replace with the actual property names
                "data2": msg.data2     # Replace with the actual property names
            }
            return jsonify(midi_data), 200
    else:
        abort(400)

def run_flask():
    app.run(host="0.0.0.0", port=port)

def midi_listener():
    global msg
    while True:
        try:
            raw_data = conn.read()
            if raw_data is not None:
                # Print raw data for debugging
                print(f"Raw MIDI Data: {raw_data}")

                # procces midi over to int
                if("ProgramChange" in msg.status):
                    print("yeha de")
                
                if("ControlChange" in msg.status):
                    print("yeha na")

                # Assign the raw_data to msg
                msg = raw_data  # raw_data is expected to be a MIDI message object

                # Example of converting raw_data to something JSON serializable
                print(f"Processed MIDI Message: status={msg.status}, data1={msg.data1}, data2={msg.data2}")

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
