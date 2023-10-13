
import numpy as np
import matplotlib.pyplot as plt

def convert_range(value, in_min, in_max, out_min, out_max):
    l_span = in_max - in_min
    r_span = out_max  - out_min
    scaled_value = (value - in_min) / l_span
    scaled_value = out_min + (scaled_value * r_span)
    return np.round(scaled_value)

result = convert_range(5, 0, 10, 0, 100)
print(result)

def modulation_shape(repeat = 1):
    # Shows the modulation shape
    t = np.arange(0, 80, 0.1)
    amplitude = np.cos(t)
    plt.plot(t[1:60], amplitude[1:60])
    plt.title("Modulation Shape")
    plt.xlabel('Time')
    plt.ylabel('Amplitude = sin(time)')
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.show()
    print(amplitude)
    return amplitude
    
amp = modulation_shape(1)

converted_amplitude = []
for number in amp:
    result = convert_range(number, -1, 1, 0, 127)
    converted_amplitude.append(result)
    
print(converted_amplitude)