#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020

@author: hassi
"""

# Let's start by importing all we need.
import numpy as np
from math import sqrt

print("Ch 2: Quantum gates")
print("-------------------")

# Set up the basic matrices
print("Vector representations of our qubits:")
print("-------------------------------------")

qubits = {"|0\u27E9":np.array([1,0]), "|1\u27E9":np.array([0,1]), "(|0\u27E9+|1\u27E9)/\u221a2":1/sqrt(2)*np.array([1,1])}

for q in qubits:
  print(q, "\n", qubits[q].round(3)) 

input("Press return to continue...\n")

print("Matrix representations of our quantum gates:")
print("--------------------------------------------")
gates ={"id":np.array([[1, 0], [0, 1]]),"x":np.array([[0, 1], [1, 0]]), "h":1/sqrt(2)*np.array([[1, 1], [1, -1]])}

for g in gates:
  print(g, "\n", gates[g].round(3)) 

# Now, let's apply the defined gates on our qubits.
# Matrix manipulations

input("Press return to continue...\n")

print("Gate manipulations of our qubits:")
print("---------------------------------")

for g in gates:
    print("Gate:",g) 
    for q in qubits:
        print(q,"\n",qubits[q].round(3),"->", np.dot(gates[g],qubits[q]).round(3)) 
    print("\n")

input("Press return to continue...\n")

print("Vector representations of our two qubits:")
print("-----------------------------------------")

twoqubits = {"|00\u27E9":np.array([1,0,0,0]), "|01\u27E9":np.array([0,1,0,0]),"|10\u27E9":np.array([0,0,1,0]),"|11\u27E9":np.array([0,0,0,1]),"|PH\u27E9":np.array([0.5,-0.5,0.5,-0.5])}

for b in twoqubits:
  print(b, "\n", twoqubits[b]) 

input("Press return to continue...\n")

print("Matrix representations of our quantum gates:")
print("--------------------------------------------")
twogates ={"cx":np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]), "swap":np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])}

for g in twogates:
  print(g, "\n", twogates[g].round()) 

input("Press return to continue...\n")

# Matrix manipulations

print("Gate manipulations of our qubits:")
print("---------------------------------")

for g in twogates:
    print("Gate:",g) 
    for b in twoqubits:
        print(b,"\n",twoqubits[b],"->", np.dot(twogates[g],twoqubits[b])) 
    print("\n")
