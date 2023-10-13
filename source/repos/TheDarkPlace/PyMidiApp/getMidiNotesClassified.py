import rtmidi


# initialise midi in class
midi_in = rtmidi.MidiIn()

# connect to a device
midi_in.open_port(0)

class MidiInputBroker:
    def __init__(self, mini_in, midiPort, noteArray):
        self.midi_in = rtmidi.MidiIn()
        self.miniPort = midiPort
        self.noteArray = noteArray
        
    def getMidiNotes(currentNotes):
        while True:    
            # Get a message, returns None if there's no msg in the queue
            # Also include the time since the last msg
            msg_and_dt = midi_in.get_message()

            # Check to see if there is a message
            if msg_and_dt:
                # Unpack the msg and time tuple
                (msg, dt) = msg_and_dt
            

                # Convert the command integer to a hex so it's easier to read
                command = hex(msg[0])

                # Print the MIDI message data and time delta
                print(f"Message: {msg} | dt = {dt:.2f}")
                if(msg[2] == 0 ):
                    # melody = ([],[])
                    currentNotes.remove(msg[1])
                    
                else:

                    # Extract the note value from the message
                    note_value = msg[1]


                    # Check if the note value is not already in uniqueReceivedNotes
                    if note_value not in uniqueReceivedNotes:
                        if(msg[2] == 0):
                            uniqueReceivedNotes.pop(note_value)
                        else:
                        # Add the note value to the list
                        # currentNotes.append(msg[1])
                            uniqueReceivedNotes.append(note_value)
                
                    else:
                        break

                    # Print the updated list of unique received note values
                    print(f"Unique Received Notes: {uniqueReceivedNotes}")
        

            else:
                # Add a short sleep so the while loop doesn't hammer your CPU
                time.sleep(0.001)
                break
        
        