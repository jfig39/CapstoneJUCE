import threading
import time
import rtmidi
from rtmidi.midiconstants import (CONTROL_CHANGE)
from  scipy import signal
import sys

import numpy as np
import matplotlib.pyplot as plt
from rtmidi.midiutil import open_midiinput
from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON

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
BPM = 90 
CHANNEL = 2
CC_NUM = 1

def convert_range(value, in_min, in_max, out_min, out_max):
    l_span = in_max - in_min
    r_span = out_max  - out_min
    scaled_value = (value - in_min) / l_span
    scaled_value = out_min + (scaled_value * r_span)
    return np.round(scaled_value)

def play_melody(melody, bpm):
    # A function which loops over the melody list
    for pitch, duration in melody:
        note_on = [0x90, pitch, 112]
        note_off = [0x80, pitch , 0]
        midiout.send_message(note_on)
        dur = duration_to_time_delay(duration, bpm)
        print(f'Sleep for {dur} seconds')
        time.sleep(dur)
        midiout.send_message(note_off)
        
def play_modulation(y, max_duration):
    # Send the modulation shape
    pause_duration = max_duration / y.size
    for v in y:
        v = convert_range(v, -1.0, 1.0, 0, 127)
        print(f"Mod: {v}")
        mod = ([CONTROL_CHANGE | CHANNEL, CC_NUM, v])
        midiout.send_message(mod)
        time.sleep(pause_duration)
        
         
    

def modulation_shape(shape: str, period: float, max_duration: float):
    # Shows the modulation shape
    
    x = np.arange(0, max_duration, 0.01)
    y=1
    
    
    if shape == 'sine':
        y = np.sin(2 * np.pi / period * x)
    elif shape == 'saw':
        y = signal.sawtooth(2 * np.pi / period * x)
    elif shape == 'square':
         y = signal.square(2 * np.pi / period * x)
    else:
        raise ValueError("Shape not supported: {shape}")
        
    plt.plot(x, y)
    plt.ylabel(f"Amplitude = {shape} (time)")
    plt.xlabel("Time")
    plt.title('Modulation Shape')
    plt.axhline(y = 0, color = 'blue')
    plt.show()
    return y
    
 
def duration_to_time_delay(duration, bpm):
    if duration == 'w':
        factor = 4
    elif duration == 'h':
        factor = 2
    elif duration == 'q':
        factor = 1
    elif duration == 'e':
        factor = 0.5
    elif duration == 's':
        factor = 0.25
    else:
        assert False
    bps = bpm / 60
    return factor * bps



# List comprehension
def duration_of_melody(melody, bpm):
    return sum(duration_to_time_delay(duration, bpm) for _, duration in melody)

   
    
   
# def main():   
#     melody = [(60, "e"),(62, "e"), (67, "q"), (62, "q"), (67, "q")] * 8
#     dur = duration_of_melody(melody, BPM)
#     print(f"Duration of melody: {dur} seconds")
#     modulation = modulation_shape("sine", period=4, max_duration=dur)
#     t1 = threading.Thread(target=play_melody, args=(melody, BPM))
#     t2 = threading.Thread(target=play_modulation, args=(modulation, dur))
#     t1.start()
#     t2.start()
####################################

def getNotes():
    # Initialize an empty list to store unique note values
    uniqueReceivedNotes = []
    note_value = 0

    while True:
        noteArray = []
        msg_and_dt = midiin.get_message()

        # Check to see if there is a message
        if msg_and_dt:
            # Unpack the msg and time tuple
            (msg, dt) = msg_and_dt

            # Convert the command integer to a hex so it's easier to read
            command = hex(msg[0])

            # Print the MIDI message data and time delta
            #print(f"Message: {msg} | dt = {dt:.2f}")

            # Extract the note value from the message
            note_value = msg[1]

            # Check if the note value is not already in uniqueReceivedNotes
           

        else:
            # Add a short sleep so the while loop doesn't hammer your CPU
            time.sleep(0.001)

        # Print the updated list of unique received note values
        print(f"Unique Received Notes: {note_value}")
        return  note_value

        # Check if you want to return the list of unique notes at this point
        # (returning inside the loop will cause the function to exit)
        # You can choose to return it here or after the loop as needed

# Example usage:
# notes = getNotes()
# print(notes)







   


     
# main()






#modulation_shape("saw", 1.0, 2.0)




####################################
# Initialize a list to save unique received note values while preserving order
uniqueReceivedNotes = []
noteDur = []
notesToArp = []
durationType = 'q'

notesToArp = set()  # Initialize a set to store unique notes

while True:
    received_notes = getNotes()
    
    for note in received_notes:
        if note not in notesToArp:
            notesToArp.add(note)  # Add unique notes to the set

    print(notesToArp)
    time.sleep(1)
    
    
       
            
    
        
