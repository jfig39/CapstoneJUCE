import time
import threading

def my_thread_function1():
    for i in range(10):
        print('1')
        time.sleep(0.1)
        
def my_thread_function2():
    for i in range(10):
        print('2')
        time.sleep(0.1)
       
my_thread1 = threading.Thread(target=my_thread_function1)
my_thread2 = threading.Thread(target=my_thread_function2)

my_thread1.start()
my_thread2.start()