#!/bin/bash
c++ $(pkg-config libevdev --libs --cflags) -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) wrapper.cpp -o libvirtinput$(python3-config --extension-suffix)
