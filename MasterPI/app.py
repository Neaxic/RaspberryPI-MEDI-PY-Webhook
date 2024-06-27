# MASTER RASPBERY PI 4 SCRIPT
# SCRIPT TO RECIVE MEDI SIGNAL, TRANSLATE IT, AND BROADCAST IT TO X

import serial
import time
import subprocess
from flask import Flask, request, abort



ser = serial.Serial('/dev/serial0', baudrate=38400)
channel = 0 # this represents channel 1
note = 60 # C4
velocity = 85
note_off = 8
note_on = 9

while True:
  print(ser)
  msg_note_on  = bytearray([(note_on << 4) | channel, note, velocity])
  msg_note_off = bytearray([(note_off << 4) | channel, note, velocity])
  print(str(hex(msg_note_on[0]))+' '+str(msg_note_on[1])+' '+str(msg_note_on[2]))
  ser.write(msg_note_on)
  time.sleep(0.5)
  ser.write(msg_note_off)
  time.sleep(0.5)