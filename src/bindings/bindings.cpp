#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>

#include "hal/crazyflie/backend.hpp"
#include "hal/i_drone_backend.hpp"
#include "hal/types.hpp"

namespace py = pybind11;
using namespace wut_control::hal;

namespace {

    void hello_drone() {
        std::cout << "Hello World!" << std::endl;
    }

}  // namespace

PYBIND11_MODULE(_core, m) {
    m.doc() = "Core C++ HAL bindings for wut_control";

    m.def("hello_drone", &hello_drone, "Print hello message from cpp");

    py::class_<DroneInfo>(m, "DroneInfo")
        .def(py::init<>())
        .def_readwrite("uri", &DroneInfo::uri)
        .def_readwrite("channel", &DroneInfo::channel)
        .def_readwrite("address", &DroneInfo::address)
        .def("__repr__", [](const DroneInfo& info) {
            return "<DroneInfo uri='" + info.uri + "' channel=" + std::to_string(info.channel) +
                   ">";
        });

    py::class_<IDroneBackend>(m, "IDroneBackend")
        .def("scan", &IDroneBackend::scan, py::arg("start_channel") = 0,
             py::arg("end_channel") = 125, py::arg("address") = 0xE7E7E7E7E7ULL,
             py::call_guard<py::gil_scoped_release>())
        .def("connect", &IDroneBackend::connect, py::arg("uri"),
             py::call_guard<py::gil_scoped_release>())
        .def("disconnect", &IDroneBackend::disconnect, py::call_guard<py::gil_scoped_release>())
        .def("is_connected", &IDroneBackend::isConnected)
        .def("emergency_stop", &IDroneBackend::emergencyStop,
             py::call_guard<py::gil_scoped_release>());

    py::class_<CrazyflieBackend, IDroneBackend>(m, "CrazyflieBackend")
        .def(py::init<>());
}