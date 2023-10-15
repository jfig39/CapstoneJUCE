import threading
import rtmidi
import time
from rtmidi.midiconstants import CONTROL_CHANGE
from scipy import signal
import sys
import numpy as np


# Sample class
class MidiModulationPlayer:
    def __init__(self, port_name=0, channel=0, cc_num=75, bpm=30, rate='w', min_val=80, max_val=127, shape="sine"):
        self.midiout = rtmidi.MidiOut()
        available_ports = self.midiout.get_ports()
        if available_ports:
            self.midiout.open_port(1)
        else:
            print(f"Could not find {port_name} in available ports. Opening the first port.")
            self.midiout.open_port(1)
   
        self.port_name = port_name
        self.channel = channel
        self.cc_num = cc_num
        self.bpm = bpm
        self.rate = rate
        self.min_val = min_val
        self.max_val = max_val
        self.shape = shape
        self.print_event = threading.Event()
        self.print_event.set()
        self.lock = threading.Lock()

    def update_parameters(self,port_name, channel, cc_num, bpm, rate, min_val, max_val, shape):
        with self.lock:
            self.port_name = port_name
            self.channel = channel
            self.cc_num = cc_num
            self.bpm = bpm
            self.rate = rate
            self.min_val = min_val
            self.max_val = max_val
            self.shape = shape

    def print_parameters_loop(self):
        while True:
            while self.print_event.is_set():
                with self.lock:
                    print(f"Channel: {self.channel}, CC Num: {self.cc_num}, BPM: {self.bpm}, Rate: {self.rate}, Min Val: {self.min_val}, Max Val: {self.max_val}, Shape: {self.shape}")
                time.sleep(1)
                
    def play_modulation(self, y, max_duration):
        pause_duration = max_duration / y.size

        for v in y:
            v = self.convert_range(v, -1.0, 1.0, 0, 127)
            v = self.convert_range(v, 0, 127, self.min_val, self.max_val)
            # print(f"Mod: {v}")
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
        bps = 60 / int(self.bpm)
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

# Function to take user input and update the data
def get_user_input(obj):
    while True:
        command = input("Enter 'start' to start printing, 'stop' to stop printing, 'play' to play modulation, or 'update' to update parameters: ")
        if command == "start":
            obj.print_event.set()
        elif command == "stop":
            obj.print_event.clear()
        elif command == "play":
            shape = input("Enter modulation shape (sine/saw/square): ")
            period = float(input("Enter period: "))
            max_duration = float(input("Enter max duration: "))
            signal_invert = input("Invert the signal? (True/False): ").lower() in ['true', 't', 'yes', 'y']
            play_thread = threading.Thread(target=obj.play_modulation_loop, args=(shape, period, max_duration, signal_invert))
            play_thread.start()
        elif command == "update":
            port_name = input("Enter port number")
            channel = int(input("Enter new channel: "))
            cc_num = int(input("Enter new cc_num: "))
            bpm = input("Enter new bpm: ")
            rate = input("Enter new rate: ")
            min_val = int(input("Enter new min_val: "))
            max_val = int(input("Enter new max_val: "))
            shape = input("Enter new shape: ")
            obj.update_parameters(port_name, channel, cc_num, bpm, rate, min_val, max_val, shape)
        else:
            print("Invalid command.")

# Create an instance of the class
my_object = MidiModulationPlayer()

# Create a thread that calls the function with the object as an argument
input_thread = threading.Thread(target=get_user_input, args=(my_object,))
print_thread = threading.Thread(target=my_object.print_parameters_loop)


# Start both threads
input_thread.start()
print_thread.start()

# Join both threads to the main thread
input_thread.join()
print_thread.join()
