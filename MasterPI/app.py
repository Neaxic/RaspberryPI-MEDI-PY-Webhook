# MASTER RASPBERY PI 4 SCRIPT
# SCRIPT TO RECIVE MEDI SIGNAL, TRANSLATE IT, AND BROADCAST IT TO X

# MEDI MARKDOWN

# API MARKDOWN
# To communicate with the rest of the RPi's, we use this master PI as the API host.
# The Slaves with x interval, will req the API for the latest data.
# This allows for unlimited scaling - it will however have a slight delay on the slaves, but should not be a problem.


#pip3 install py-midi

from midi import MidiConnector
# import os
# import subprocess
# from flask import Flask, request, abort

# app = Flask(__name__)

conn = MidiConnector('/dev/serial0')
note = 70
channel = 0
msg = None # overwritten by read()
port = 2000
password = "asdl" # maybe not even have one

# @app.route('/master', methods=['GET'])
# def webhook():
#     query_password = request.args.get('password', '')  # Defaults to empty string if not found
#     if query_password != password:
#         return "Unauthorized", 401  # Unauthorized access

#     if request.method == 'GET':
#         print(request.json)
#         return msg, 200
#     else:
#         abort(400)

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=port)

while True:
  try:
    msg = conn.read()
    print(msg)
    # API SHIT

  except TypeError:
    print("MIDI read error")





