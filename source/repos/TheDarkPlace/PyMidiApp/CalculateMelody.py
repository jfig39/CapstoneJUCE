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

def convert_range(value, in_min, in_max, out_min, out_max):
    l_span = in_max - in_min
    r_span = out_max  - out_min
    scaled_value = (value - in_min) / l_span
    scaled_value = out_min + (scaled_value * r_span)
    return np.round(scaled_value)


def send_mod(amplitude, repeat):
    #A function which will send CC data to a MIDI driver
    scaled = []
    for amp in amplitude:
        val = (convert_range(amp, -1, 1.0, 0, 127))
        scaled.append(val)
    for _ in range(repeat):
        for value in scaled:
            mod = ([CONTROL_CHANGE | CHANNEL, CC_NUM, value])
            midiout.send_message(mod)
            time.sleep(SPEED)
            
BPM = 60         
    

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
        print("That wave is not supported")
        sys.exit()
        
    plt.plot(x, y)
    plt.ylabel(f"Amplitude = {shape} (time)")
    plt.xlabel("Time")
    plt.title('Modulation Shape')
    plt.axhline(y = 0, color = 'blue')
    plt.show()
    
 
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

# def  duration_of_melody(melody, bpm):
#     t = 0
#     for _, duration in melody:
#         t += duration_to_time_delay(duration, bpm)
#     return t

# List comprehension
def duration_of_melody(melody, bpm):
    return sum(duration_to_time_delay(duration, bpm) for _, duration in melody)
    #     print(f"We need towait for {t} seconds")
    # print("Total time: ", t)
   
    
   
def main():   
    melody = [(60, "e"),(62, "e"), (67, "q"), (62, "q"), (67, "q")] * 8
    dur = duration_of_melody(melody, BPM)
    print(f"Duration of melody: {dur} seconds")
     
main()





#modulation_shape("saw", 1.0, 2.0)



