"""
    Keys lesson

    Objects in Python
    Objects in PySimpleGUI
        http://calls.PySimpleGUI.org - Call reference lists objects and member functions
    Keys in PySimpleGUI
        1. Identify elements - like an element's "Name", so they need to be unique
        2. Events are usually keys
        3. Used as Keys in "values dictionary"
    Keys can be:
        1. Anything that's "Hashable" (basically not a "list". Tuple is OK though)
        2. Common Key types:
            * String is most common (coding convention "-KEY-")
            * Tuples - One use is when layout is a grid of something
            * Numbers - used with auto-numbered keys
            * Functions (used with custom dispatcher)
            * Can't be None (WIN_CLOSED event == None) and None is special parameter value in PySimpleGUI
    Keys are specified using "key" keyword when element is created
    NEW Element - The Input Element - get a line of text. Your 3rd element (only 24 more to learn)
    Finding elements using keys:
        1. window[key]
        2. window.find_element(key)
    Downside to finding elements is missing auto-completion in PyCharm
        Saving variable with element definition gets around this

"""

import PySimpleGUI as sg

input1 = sg.Input(key='-IN1-')

layout = [[sg.Text('This is a text element')],
          [input1],
          [sg.Input(key='-IN2-')],
          [sg.Button('Ok', key='-OK-'), sg.Button('Exit')]]

window = sg.Window('Title', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    input1.update()

window.close()

