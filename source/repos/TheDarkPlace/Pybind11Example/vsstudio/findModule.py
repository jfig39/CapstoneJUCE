import sys

# Add the directory to sys.path
directory_to_add = r'C:\Users\j0sef\source\repos\TheDarkPlace\Pybind11Example\vsstudio\Debug'
sys.path.append(directory_to_add)

# Now you can import modules from the added directory
import pybind11module

pybind11module.say_hello()
