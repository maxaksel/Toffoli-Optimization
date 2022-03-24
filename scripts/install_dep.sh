#!/bin/bash

conda create -n micro python=3.9
conda activate micro
pip install numpy
pip install scipy
pip install qiskit==0.32.1
pip install cirq
pip install cirq-superstaq==0.1.16

