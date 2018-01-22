#!/bin/bash

git clone --recursive https://github.com/matrix-io/matrix-creator-hal.git

cd matrix-creator-hal && mkdir build && cd build

cmake ..

make && sudo make install
