import time
import rtmidi
from rtmidi.midiconstants import CONTROL_CHANGE
from scipy import signal
import sys
import numpy as np
import matplotlib.pyplot as plt
import threading

class MidiModulationPlayer:
    def __init__(self, midiout, channel=0, cc_num=75, speed=0.05, bpm=30, rate='w', min_val=80, max_val=127):
        self.midiout = midiout
        self.channel = channel
        self.cc_num = cc_num
        self.speed = speed
        self.bpm = bpm
        self.rate = rate
        self.min_val = min_val
        self.max_val = max_val

    def play_modulation(self, y, max_duration):
        pause_duration = max_duration / y.size

        for v in y:
            v = self.convert_range(v, -1.0, 1.0, 0, 127)
            v = self.convert_range(v, 0, 127, self.min_val, self.max_val)
            print(f"Mod: {v}")
            mod = ([CONTROL_CHANGE | self.channel, self.cc_num, v])
            self.midiout.send_message(mod)
            time.sleep(pause_duration)

    def modulation_shape(self, shape, period, max_duration, signal_invert):
        x = np.arange(0, max_duration, 0.01)
        y = 1
        sig_invert = 1

        if signal_invert:
            sig_invert = -1

        if shape == 'sine':
            y = sig_invert * np.sin(2 * np.pi / period * x)
        elif shape == 'saw':
            y = sig_invert * signal.sawtooth(2 * np.pi / period * x)
        elif shape == 'square':
            y = sig_invert * signal.square(2 * np.pi / period * x)
        else:
            print("That wave is not supported")
            sys.exit()

        return y

    def duration_to_time_delay(self, duration):
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
        bps = 60 / self.bpm
        return factor * bps

    def play_modulation_loop(self, shape, period, max_duration, signal_invert):
        dur = self.duration_to_time_delay(self.rate)
        modulation = self.modulation_shape(shape, period, max_duration, signal_invert)
        while True:
            self.play_modulation(modulation, dur)

    def convert_range(self, value, in_min, in_max, out_min, out_max):
        l_span = in_max - in_min
        r_span = out_max - out_min
        scaled_value = (value - in_min) / l_span
        scaled_value = out_min + (scaled_value * r_span)
        return np.round(scaled_value)

# Usage example
if __name__ == "__main__":
    # Initialize the MIDI port outside of the class
    midiout = rtmidi.MidiOut()
    midiout.open_port(1)

    # Create instances of MidiModulationPlayer with the same MIDI port
    player1 = MidiModulationPlayer(midiout, channel=0, cc_num=75, speed=0.05, bpm=30, rate='w', min_val=60, max_val=70)
    player2 = MidiModulationPlayer(midiout, channel=1, cc_num=76, speed=0.05, bpm=40, rate='h', min_val=0, max_val=127)

    # Start threads for both players
    thread1 = threading.Thread(target=player1.play_modulation_loop, args=("sine", 1.0, 2.0, False))
    thread2 = threading.Thread(target=player2.play_modulation_loop, args=("saw", 1.0, 2.0, False))
    thread1.start()
    thread2.start()
