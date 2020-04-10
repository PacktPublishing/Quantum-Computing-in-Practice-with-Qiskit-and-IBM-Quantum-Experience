#!/usr/bin/env python
# coding: utf-8

# Let's start by importing numpy and math.
import numpy as np
from math import sqrt, pow

print("Ch 2: Bits and qubits")
print("---------------------")

# Define the qubit parameters for superposition
a = sqrt(1/2)
b = sqrt(1/2)

if round(pow(a,2)+pow(b,2),0)!=1:
    print("Your qubit parameters are not normalized.\nResetting to basic superposition")
    a = sqrt(1/2)
    b = sqrt(1/2)

# Set up the bit and qubit vectors

bits = {"bit = 0":np.array([1,0]), "bit = 1":np.array([0,1]), "|0>":np.array([1,0]), "|1>":np.array([0,1]), "(|0>+|1>)/\u221a2":np.array([a,b])}

# Print the vectors 
for b in bits:
  print(b, ": ", bits[b]) 
print ("\n")

# Do a "measurement" of the bits and qubits
print("'Measuring' our bits and qubits")
print("-------------------------------")

# Create a measurement dictionary 
prob={}

for b in bits:
    print(b)
    print("Probability of getting:")
    for dig in range(len(bits[b])):
        prob[b]=pow(bits[b][dig],2)
        print(dig, " = ", '%.2f'%(prob[b]*100), "percent") 
    print ("\n")

