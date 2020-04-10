#!/usr/bin/env python
# coding: utf-8
# ch2_r4_reversible_gates.py

import numpy as np
from math import sqrt

# Set up the basic matrices

print("Ch 2: Reversible quantum gates")
print("------------------------------")

qubits = {"|0>":np.array([1,0]), "|1>":np.array([0,1]), "(|0>+|1>)/\u221a2":1/sqrt(2)*np.array([1,1])}

for q in qubits:
  print(q, "\n", qubits[q]) 
print ("\n")

print("Matrix representations of our gates:")
print("-------------------------------------")
#gates ={"id":np.array([[1, 0], [0, 1]]),"x":np.array([[0, 1], [1, 0]]), "y":np.array([[0, -1.j], [1.j, 0]]), "z":np.array([[1, 0], [0, -1]]), "h":1/sqrt(2)*np.array([[1, 1], [1, -1]])}
gates ={"id":np.array([[1, 0], [0, 1]]),"x":np.array([[0, 1], [1, 0]]), "h":1/sqrt(2)*np.array([[1, 1], [1, -1]])}

for g in gates:
  print(g, "\n", gates[g].round(3)) 
print ("\n")


# Demonstrate that the basic quantum gates are reversible. For example: <x|q|x> = q, and <h|q|h> = q

# Reversible gates

for g in gates:
    print("Gate:",g) 
    print("-------")
    for q in qubits:
        print ("\nOriginal qubit: ",q,"\n", qubits[q].round(3))
        print ("Qubit after",g,"gate: \n",np.dot(gates[g],qubits[q]).round(3))
        print ("Qubit after two",g,"gates. Back in:",q,"\n",np.dot(np.dot(gates[g],qubits[q]),gates[g]).round(3))
    print("\n")


# And mathematically, by showing that X•X = I (Identity matrix)

# Reversible gate results in identity matrix

for g in gates:
    print("\nGate:",g, "\n--------\n", gates[g]) 
    print ("\n",g,"•",g,"\n",np.dot(gates[g],gates[g]).round())
print ("\n")





