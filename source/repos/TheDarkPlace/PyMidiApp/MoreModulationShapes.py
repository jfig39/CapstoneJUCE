import time
import rtmidi
from rtmidi.midiconstants import (CONTROL_CHANGE)
from  scipy import signal
import sys


import numpy as np
import matplotlib.pyplot as plt

midiout = rtmidi.MidiOut()
midiout.open_port(2)

CHANNEL = 0
CC_NUM = 75
SPEED = 0.05
BPM = 120

def convert_range(value, in_min, in_max, out_min, out_max):
    l_span = in_max - in_min
    r_span = out_max  - out_min
    scaled_value = (value - in_min) / l_span
    scaled_value = out_min + (scaled_value * r_span)
    return np.round(scaled_value)


def send_mod(amplitude, repeat):
    #A function which will send CC data to a MIDI driver
    scaled = []
    bps = 60 / BPM
    for amp in amplitude:
        val = (convert_range(amp, -1, 1.0, 0, 127))
        scaled.append(val)
    for _ in range(repeat):
        for value in scaled:
            mod = ([CONTROL_CHANGE | CHANNEL, CC_NUM, value])
            midiout.send_message(mod)
            time.sleep(SPEED)
            
            
    

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
        
    plt.plot(x, y)
    plt.ylabel(f"Amplitude = {shape} (time)")
    plt.xlabel("Time")
    plt.title('Modulation Shape')
    plt.axhline(y = 0, color = 'blue')
    plt.show()
    
    
               
    print(x)
    
   
    
modulation_shape("saw", 1.0, 2.0, True)




