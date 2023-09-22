#include <Windows.h>
#include <iostream>
#include <string>
#include <Python.h>


using namespace std;

// https://docs.python.org/3/extending/embedding.html
void CallPython(string PythonModuleName, string PythonFunctionName)
{
	char* funcname = new char[PythonFunctionName.length() + 1];
	strcpy_s(funcname, PythonFunctionName.length() + 1, PythonFunctionName.c_str());

	char* modname = new char[PythonModuleName.length() + 1];
	strcpy_s(modname, PythonModuleName.length() + 1, PythonModuleName.c_str());

	printf("Hit any key to initialize the Python interpreter\n");
	system("pause");

	// Initialize the Python interpreter 
	// https://docs.python.org/3/c-api/init.html#c.Py_Initialize
	Py_Initialize();

	TCHAR cwd[2048];
	GetCurrentDirectory(sizeof(cwd), cwd);

	// Import a module. This is best described by referring to the built-in Python function __import__().
	// https://docs.python.org/3/c-api/import.html?highlight=pyimport_importmodule#c.PyImport_ImportModule 
	printf("Hit any key to Load the Python module %ws - %s\n", cwd, modname);
	system("pause");
	PyObject* my_module = PyImport_ImportModule(modname);

	// Print a standard traceback to sys.stderr and clear the error indicator
	// https://docs.python.org/3/c-api/exceptions.html?highlight=pyerr_print#c.PyErr_Print
	PyErr_Print();

	printf("Module found\n");
	printf("Hit any key to find function %s from Python module %ws\n", funcname, cwd);
	system("pause");

	// Get the address of the particular Python function in the imported module
	// https://docs.python.org/3/c-api/object.html?highlight=pyobject_getattrstring#c.PyObject_GetAttrString
	printf("Getting address of %s in Python module\n", funcname);
	PyObject* my_function = PyObject_GetAttrString(my_module, funcname);

	PyErr_Print();

	printf("Function found\n");
	printf("Hit any key to call function %s from Python module %ws\n", funcname, cwd);
	system("pause");

	// Call a callable Python object callable, with arguments given by the tuple args. 
	// If no arguments are needed, then args can be NULL.
	// https://docs.python.org/3/c-api/call.html?highlight=pyobject_callobject#c.PyObject_CallObject
	PyObject* my_result = PyObject_CallObject(my_function, NULL);

	PyErr_Print();

	printf("Your function has been called\n");
	system("pause");

	// Undo all initializations made by Py_Initialize() and subsequent use of Python/C API functions, 
	// and destroy all sub-interpreters (see Py_NewInterpreter() below) that were created and not yet 
	// destroyed since the last call to Py_Initialize(). Ideally, this frees all memory allocated by the Python interpreter.
	// https://docs.python.org/3/c-api/init.html?highlight=py_finalize#c.Py_FinalizeEx
	Py_Finalize();

	delete[] funcname;
	delete[] modname;
}

int main()
{
	CallPython("PythonFile", "helloworld");
	system("pause");
	return 0;
}

/* Python code
import re
import string
def helloworld():
	print("Hello from Python!")
*/