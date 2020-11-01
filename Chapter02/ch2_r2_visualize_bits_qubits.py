#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020

@author: hassi
"""

# Let's start by importing numpy and math.
import numpy as np
import cmath 
from math import pi, sin, cos
from qiskit.visualization import plot_bloch_vector

np.set_printoptions(precision=3)

print("Ch 2: Bloch sphere visualization of bits and qubits")
print("----------------------------------------------------")

# Superposition with zero phase
angles={"theta": pi/2, "phi":0}

# Self-defined qubit
#angles["theta"]=float(input("Theta:\n"))
#angles["phi"]=float(input("Phi:\n"))

# Set up the bit and qubit vectors
bits = {"bit = 0":{"theta": 0, "phi":0}, "bit = 1":{"theta": pi, "phi":0}, "|0\u27E9":{"theta": 0, "phi":0}, "|1\u27E9":{"theta": pi, "phi":0}, "a|0\u27E9+b|1\u27E9":angles}

# Print the bits and qubits on the Bloch sphere 
for bit in bits:
    bloch=[cos(bits[bit]["phi"])*sin(bits[bit]["theta"]),sin(bits[bit]["phi"])*sin(bits[bit]["theta"]),cos(bits[bit]["theta"])]
    display(plot_bloch_vector(bloch, title=bit))
    # Build the state vector
    a = cos(bits[bit]["theta"]/2)
    b = cmath.exp(bits[bit]["phi"]*1j)*sin(bits[bit]["theta"]/2)
    state_vector = [a * complex(1, 0), b * complex(1, 0)]
    print("State vector:", np.around(state_vector, decimals = 3))