#include <pybind11/embed.h>
namespace py = pybind11;

void say_something()
{
    printf("Say Something\n");
}

static int COUNTER = 0;
void set_counter(int count)
{
    COUNTER = count;
}

PYBIND11_EMBEDDED_MODULE(embeddedmodule, module)
{
    module.doc() = "Embedded Module";
    module.def("say_something", &say_something);
    module.def("set_counter", &set_counter);
}

int main()
{
    py::scoped_interpreter guard{};

    try {
        py::exec("print('hello jose')");
        py::exec("import embeddedmodule\nembeddedmodule.say_something()");
        py::exec("embeddedmodule.set_counter(10)");

        auto sys = pybind11::module::import ("sys");
        pybind11::print(sys.attr("path"));

        {
            auto hello_module = pybind11::module::import ("hello");
        }
    }
    catch (const py::error_already_set& e) {
        PyErr_Print(); // Print Python error information
        return 1; // Return an error code if Python exceptions occur
    }

    return 0;
}
