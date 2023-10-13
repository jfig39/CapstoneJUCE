import time
import rtmidi
from rtmidi.midiconstants import (CONTROL_CHANGE)
from  scipy import signal
import sys


import numpy as np
import matplotlib.pyplot as plt

midiout = rtmidi.MidiOut()
midiout.open_port(1)

CHANNEL = 0
CC_NUM = 75
SPEED = 0.05
BPM = 30 
RATE = 'w'
minVal = 80
maxVal= 127

def convert_range(value, in_min, in_max, out_min, out_max):
    l_span = in_max - in_min
    r_span = out_max  - out_min
    scaled_value = (value - in_min) / l_span
    scaled_value = out_min + (scaled_value * r_span)
    return np.round(scaled_value)


# def send_mod(amplitude, repeat):
#     #A function which will send CC data to a MIDI driver
#     scaled = []
#     bps = 60 / BPM
#     for amp in amplitude:
#         val = (convert_range(amp, -1, 1.0, 0, 127))
#         scaled.append(val)
#     for _ in range(repeat):
#         for value in scaled:
#             mod = ([CONTROL_CHANGE | CHANNEL, CC_NUM, value])
#             midiout.send_message(mod)
#             time.sleep(SPEED)
            
def play_modulation(y, max_duration, rangeMin, rangeMax):
    # Send the modulation shape
    pause_duration = max_duration / y.size
    for v in y:
        v = convert_range(v, -1.0, 1.0, 0, 127)
        v = convert_range(v, 0, 127, rangeMin, rangeMax)
        print(f"Mod: {v}")
        mod = ([CONTROL_CHANGE | CHANNEL, CC_NUM, v])
        midiout.send_message(mod)
        time.sleep(pause_duration)
            
    

def modulation_shape(shape: str, period: float, max_duration: float, signalInvert: bool):
    # Shows the modulation shape
    
    x = np.arange(0, max_duration, 0.01)
    y=1
    sigInvert = 1
    
    if(signalInvert == True):
        sigInvert = -1
    
    
    if shape == 'sine':
        y = sigInvert*np.sin(2 * np.pi / period * x)
    elif shape == 'saw':
        y = sigInvert*signal.sawtooth(2 * np.pi / period * x)
    elif shape == 'square':
         y = sigInvert*signal.square(2 * np.pi / period * x)
    else:
        print("That wave is not supported")
        sys.exit()
        
    return y
        
    # plt.plot(x, y)
    # plt.ylabel(f"Amplitude = {shape} (time)")
    # plt.xlabel("Time")
    # plt.title('Modulation Shape')
    # plt.axhline(y = 0, color = 'blue')
    # plt.show()
    
    
               
    print(x)
    
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
    bps = 60 / bpm  
    return factor * bps



# List comprehension
def duration_of_melody(melody, bpm):
    return sum(duration_to_time_delay(duration, bpm) for _, duration in melody)
    
   
dur = duration_to_time_delay(RATE, BPM)
modulation = modulation_shape("saw", 1.0, 2.0, False)
while True:
            
          
    play_modulation(modulation, dur,minVal, maxVal)
           




