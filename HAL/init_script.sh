#!/bin/bash

#add repo and key
curl https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list

# Update packages and install
sudo apt-get update
sudo apt-get upgrade

# Installation
sudo apt install libmatrixio-creator-hal libmatrixio-creator-hal-dev

sudo apt-get install cmake g++ git libfftw3-dev wiringpi matrixio-creator-init libgflags-dev