# MASTER RASPBERY PI 4 SCRIPT
# SCRIPT TO RECIVE MEDI SIGNAL, TRANSLATE IT, AND BROADCAST IT TO X

#pip3 install py-midi

import midi
import os

conn = midi.MidiConnector('/dev/serial0', baudrate=38400, timeout=1)

note = 70
channel = 0

while True:
  msg = None
  try:
    msg = conn.read()
    print(msg)
    # API SHIT




  except TypeError:
    print("MIDI read error")
