#!/usr/bin/env python
# coding: utf-8

# Let's start by importing numpy and math.
import numpy as np
from math import sqrt, pow
from qiskit.visualization import plot_bloch_vector
from IPython import display


print("Ch 2: Bloch sphere visualization of bits and qubits")
print("----------------------------------------------------")


# Define the Pauli vectors
x=np.matrix([[0,1],[1,0]])
y=np.matrix([[0,-1j],[1j,0]])
z=np.matrix([[1,0],[0,-1]])

# Superposition with zero phase
a = 1/sqrt(2)
b = 1/sqrt(2)

# Superposition with pi/8 phase angle
#a = 1/sqrt(2)
#b = 1/sqrt(2)*(0.923879533 + 0.382683432j)

if round(pow(abs(a),2)+pow(abs(b),2),0)!=1:
    print("Your qubit parameters are not normalized.\nResetting to basic superposition")
    a = 1/sqrt(2)
    b = 1/sqrt(2)

# Set up the bit and qubit vectors
bits = {"bit = 0":np.matrix([1,0]), "bit = 1":np.matrix([0,1]), "|0>":np.matrix([1,0]), "|1>":np.matrix([0,1]), "a|0>+b|1>":np.matrix([a,b])}

# Print the bits and qubits on the Bloch sphere 
for b in bits:
    bloch=[(np.trace(x*(bits[b].getH()*bits[b]))).real,(np.trace(y*(bits[b].getH()*bits[b]))).real,(np.trace(z*(bits[b].getH()*bits[b]))).real]
    file=(plot_bloch_vector(bloch, title=b))
    display(file)
    print("State vector:", bits.get(b).round(3))
