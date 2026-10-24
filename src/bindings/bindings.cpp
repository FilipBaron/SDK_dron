#include <pybind11/pybind11.h>
#include <iostream>

namespace py = pybind11;

void hello_drone() {
    std::cout << "Hello World!" << std::endl;
}

PYBIND11_MODULE(_core, m) {
    m.def("hello_drone", &hello_drone, "Print hello message from cpp");
}
