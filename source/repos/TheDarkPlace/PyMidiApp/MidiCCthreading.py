from threading import Thread
import time
import rtmidi
from rtmidi.midiconstants import CONTROL_CHANGE
import numpy as np
import sys
from scipy import signal

# Define your modulation parameters
period = 2
max_duration = 2
signal_invert = True

class CustomThread(Thread):
    def __init__(self, target=None, args=(), kwargs={}, name=None, var1=0, shape="sine", rate='w'):
        Thread.__init__(self, target=target, args=args, kwargs=kwargs, name=name)
        self._return = None
        self.var1 = var1
        self.shape = shape
        self.running = True
        self.rate = rate
        self.midiout = None
        self.midi_modulation_player = None

    def create_midi_modulation_player(self, channel, cc_num, speed, bpm, min_val, max_val):
        self.midiout = rtmidi.MidiOut()
        self.midiout.open_port(1)
        self.midi_modulation_player = self.MidiModulationPlayer(self.midiout, channel, cc_num, speed, bpm, self.rate, min_val, max_val)

    class MidiModulationPlayer:
        def __init__(self, midiout, channel=0, cc_num=75, speed=0.05, bpm=30, rate='w', min_val=0, max_val=127):
            self.midiout = midiout
            self.channel = channel
            self.cc_num = cc_num
            self.speed = speed
            self.bpm = bpm
            self.rate = rate
            self.min_val = min_val
            self.max_val = max_val
            self.running = True
   
        def play_modulation(self, y, max_duration):
            pause_duration = max_duration / y.size
            print(y.size)
            while True:
                for v in y:
                    print(v)
                    v = self.convert_range(v, -1.0, 1.0, 0, 127)
                    v = self.convert_range(v, 0, 127, self.min_val, self.max_val)
                    print(f"Mod: {v}")
                    mod = [CONTROL_CHANGE | self.channel, self.cc_num, v]
                    self.midiout.send_message(mod)
                    time.sleep(pause_duration)
                
        def convert_range(self, value, in_min, in_max, out_min, out_max):
            l_span = in_max - in_min
            r_span = out_max - out_min
            scaled_value = (value - in_min) / l_span
            scaled_value = out_min + (scaled_value * r_span)
            return int(np.round(scaled_value))
        

        def modulation_shape(self, shape, period, max_duration, signal_invert):
            x = np.arange(0, max_duration, 0.01)
            y = 1

            if shape == 'sine':
                y = np.sin(2 * np.pi / period * x)
            elif shape == 'saw':
                y = signal.sawtooth(2 * np.pi / period * x)
            elif shape == 'square':
                y = signal.square(2 * np.pi / period * x)
            else:
                print("That wave is not supported")
                sys.exit()

            if signal_invert:
                y = -y  # Invert the signal

            return y

        # Rest of the MidiModulationPlayer methods (as in your original code)

    def run(self):
        if self.midi_modulation_player is None:
            raise ValueError("MidiModulationPlayer not created. Call create_midi_modulation_player first.")

        while self.running:
            print("Custom Thread: var1 =", self.var1)
            time.sleep(1)

        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
            print("Custom Thread: Result of target function is", self._return)

    def join(self):
        self.running = False  # Signal the thread to stop
        if self.midiout:
            self.midiout.close_port()
        Thread.join(self)
        return self._return

    def updateVar(self, newVar):
        self.var1 = newVar

def add(n1, n2):
    result = n1 + n2
    return result

# Input variable values
varControl = int(input("Enter a new variable value: "))
channel = int(input("Enter MIDI channel: "))
cc_num = int(input("Enter MIDI CC number: "))
speed = float(input("Enter speed: "))
bpm = int(input("Enter BPM: "))

rate = input("Enter rate ('w', 'h', 'q', 'e', 's'): ")
while rate not in ['w', 'h', 'q', 'e', 's']:
    print("Invalid rate input. Please enter 'w', 'h', 'q', 'e', or 's'.")
    rate = input("Enter rate: ")

min_val = int(input("Enter min value: "))
max_val = int(input("Enter max value: "))

# Create a custom thread and start it
thread = CustomThread(target=add, args=(5, 4))
thread.create_midi_modulation_player(channel, cc_num, speed, bpm, min_val, max_val)
thread.start()

# Create a waveform using the modulation_shape method
waveform = thread.midi_modulation_player.modulation_shape(thread.shape, period, max_duration, signal_invert)

# Start the modulation loop within the MidiModulationPlayer
thread.midi_modulation_player.play_modulation(thread.midi_modulation_player.modulation_shape(thread.shape, period, max_duration, signal_invert), max_duration)

try:
    while True:
        print("Change the variable")
        newValue = int(input())
        thread.updateVar(newValue)
        time.sleep(3)  # Wait for 3 seconds before updating again
except KeyboardInterrupt:
    pass

# Wait for the thread to finish and get the result
result = thread.join()
print("Main Thread: Result of add function is", result)
