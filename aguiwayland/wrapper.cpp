#include <pybind11/pybind11.h>
#include "virtkeyb.cpp"
namespace py = pybind11;
PYBIND11_MODULE(libvirtinput,m)
{
    py::class_<VirtInput>(m,"VirtInput")
        .def(py::init<>())
        .def("click", &VirtInput::click)
        .def("move", &VirtInput::move)
        .def("scroll", &VirtInput::scroll)
        .def("type", &VirtInput::type)
        .def("press", &VirtInput::press);

}
