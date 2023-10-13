#!/usr/bin/env python
#
# midiin_poll.py
#
"""Show how to receive MIDI input by polling an input port."""

from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midiinput
from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON


log = logging.getLogger('midiin_poll')
logging.basicConfig(level=logging.DEBUG)

sequence = [0,1,2,3,4,5,6,7,8,9,10,11,12]
sequencePos = 0

SCALES = {
  'major': (0, 2, 4, 5, 7, 9, 11, 12),
  'minor': (0, 2, 3, 5, 7, 8, 10, 12),
  'melodicminor': (0, 2, 3, 5, 7, 9, 11, 12),
  'harmonicminor': (0, 2, 3, 5, 7, 8, 11, 12),
  'pentatonicmajor': (0, 2, 4, 7, 9, 12),
  'bluesmajor': (0, 3, 4, 5, 7, 10, 12),
  'pentatonicminor': (0, 3, 5, 7, 10, 12),
  'bluesminor': (0, 3, 4, 5, 7, 10, 12),
  'augmented': (0, 3, 4, 7, 8, 11, 12),
  'diminished': (0, 2, 3, 5, 6, 8, 9, 11, 12),
  'chromatic': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
  'wholehalf': (0, 2, 3, 5, 6, 8, 9, 11, 12),
  'halfwhole': (0, 1, 3, 4, 6, 7, 9, 10, 12),
  'wholetone': (0, 2, 4, 6, 8, 10, 12),
  'augmentedfifth': (0, 4, 5, 9, 10, 14, 15, 19),
  'japanese': (0, 4, 6, 7, 11, 12, 16, 18),
  'oriental': (0, 1, 4, 5, 7, 8, 11, 12),
  'ionian': (0, 2, 4, 5, 7, 9, 11, 12),
  'dorian': (0, 2, 3, 5, 7, 9, 10, 12),
  'phrygian': (0, 1, 3, 5, 7, 8, 10, 12),
  'lydian': (0, 2, 4, 6, 7, 9, 11, 12),
  'mixolydian': (0, 2, 4, 5, 7, 9, 10, 12),
  'aeolian': (0, 2, 3, 5, 7, 8, 10, 12),
  'locrian': (0, 1, 3, 5, 6, 8, 10, 12),
}

# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiout, port_name = open_midioutput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()
# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()
print("")    
print("Select the scale")
print("") 
print('major')
print('minor')
print('melodicminor')
print('harmonicminor')
print('pentatonicmajor')
print('bluesmajor')
print('pentatonicminor')
print('bluesminor')
print('augmented')
print('diminished')
print('chromatic')
print('wholehalf')
print('halfwhole')
print('wholetone')
print('augmentedfifth')
print('japanese')
print('oriental')
print('ionian')
print('dorian')
print('phrygian')
print('lydian')
print('mixolydian')
print('aeolian')
        
scale_input = input()
scale = SCALES[scale_input]  
print("") 
print("Select the bpm")
bpm = float(input("Enter BPM: "))  # Convert the user input to a floating-point number
noteSpeed = (60 / bpm) * (1/4) # multiply by 4 to get quarter note speed
print("Note Speed (notes per second):", noteSpeed)
print("") 

  # user_input = input("Enter characters separated by commas: ")
midiArray = []
noteSequence = []

# Split the input string into individual values
print("Set the intervals you want to play")
user_input = input()
input_values = user_input.split(',')

# Iterate through the input values and add them to the array as integers
for value in input_values:
    value = value.strip()  # Remove leading and trailing whitespace
    try:
        int_value = int(value)  # Convert the string to an integer
        midiArray.append(int_value)
        print(midiArray)                
    except ValueError:
        print(f"Skipping invalid value: {value}")

# Print the array with the integer values
print("Array with integer values:", midiArray)

print("Entering main loop. Press Control-C to exit.")
try:
    timer = time.time()
    while True:
        msg = midiin.get_message()

        if msg:
            message, deltatime = msg
            
            timer += deltatime
            message, deltatime = msg
            currentNote = message[1]
            while(message[0] == 144):
                print(sequencePos)
                currentMsg = message
                # print("[%s] @%0.6f %r Received MSG" % (port_name, timer, message))
                if(sequencePos > (len(midiArray)-1)):
                    sequencePos = 0
                    currentMsg[1] = message[1]
                note_on = [NOTE_ON, currentMsg[1], 112]  # channel 1, middle C, velocity 112
                note_off = [NOTE_OFF, currentMsg[1], 0]
                
                print("Sending NoteOn event.")
                midiout.send_message(note_on)
                time.sleep(noteSpeed)
                print("Sending NoteOff event.")
                midiout.send_message(note_off)
                time.sleep(noteSpeed)
                
               
                currentMsg[1] = currentNote + scale[midiArray[sequencePos]]
                sequencePos += 1    
            
                
                timer += deltatime
                print("[%s] @%0.6f %r Received MSG" % (port_name, timer, currentMsg))
                # with midiout:
                #     print("Sending NoteOn event.")
                #     midiout.send_message(note_on)
                #     time.sleep(1)
                #     print("Sending NoteOff event.")
                #     midiout.send_message(note_off)
                #     time.sleep(0.1)
                # time.sleep(noteSpeed)
                msg = midiin.get_message()
                if(msg):
                    break

        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin