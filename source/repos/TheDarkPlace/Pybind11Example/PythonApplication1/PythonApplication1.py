import sys
sys.path.append(r'C:\Users\j0sef\source\repos\TheDarkPlace\Pybind11Example\vsstudio\Debug')

import pybind11module  # Replace 'module_name' with the actual name of your .pyd file (without the .pyd extension)

# Use functions/classes from the .pyd module
result = module_name.some_function()

