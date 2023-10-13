from threading import Thread
import time
import midiCC

class CustomThread(Thread):
    def __init__(self, target=None, args=(), kwargs={}, name=None, var1=0, shape = "sine", rate = 'q'):
        Thread.__init__(self, target=target, args=args, kwargs=kwargs, name=name)
        self._return = None
        self.var1 = var1
        self.shape = shape
        self.running = True

    def run(self):
        while self.running:
            print("Custom Thread: var1 =", self.var1)
            time.sleep(1)

        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
            print("Custom Thread: Result of target function is", self._return)

    def join(self):
        self.running = False  # Signal the thread to stop
        Thread.join(self)
        return self._return

    def updateVar(self, newVar):
        self.var1 = newVar
    

        
    
        
    

def add(n1, n2):
    result = n1 + n2
    return result

# Input a variable value
varControl = int(input("Enter a new variable value: "))

# Create a custom thread and start it
thread = CustomThread(target=add, args=(5, 4))
thread.start()

try:
    while True:
        print("Change the variable")
        newValue = input()
        thread.updateVar(newValue)
        time.sleep(3)  # Wait for 3 seconds before updating again
except KeyboardInterrupt:
    pass

# Wait for the thread to finish and get the result
result = thread.join()
print("Main Thread: Result of add function is", result)
