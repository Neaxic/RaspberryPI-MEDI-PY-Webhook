import midi
import os
import subprocess
from flask import Flask, request, abort
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
        print(request.json)
        return msg, 200
    else:
        abort(400)

def run_flask():
    app.run(host="0.0.0.0", port=port)

def midi_listener():
    global msg
    while True:
        try:
            msg = conn.read()
            if msg is not None:
                print(msg)
        except TypeError:
            print("MIDI read error")

if __name__ == '__main__':
    # Start the Flask API server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Allows Flask thread to exit when the main program exits
    flask_thread.start()

    # Start listening to MIDI signals in the main thread
    midi_listener()
