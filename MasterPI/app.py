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

cc = 0
pc = 0

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
            return jsonify({"midi_message": msg}), 200
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
                if("ProgramChange" in str(raw_data.type)):
                    print("Program Change")
                    pc = raw_data.program_number + 1
                if("ControlChange" in str(raw_data.type)):
                    print("Control Change")
                    cc = raw_data.control_number
                
                # Process the raw MIDI data
                num = cc * 128 + pc +1

                msg = num  # Assign the processed message
                print(f"Processed MIDI Message: {msg}")
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
