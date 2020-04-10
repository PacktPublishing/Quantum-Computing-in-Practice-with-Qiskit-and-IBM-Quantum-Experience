#!/usr/bin/env python
# coding: utf-8

# Let's start by importing all we need.
import numpy as np

print("Ch 2: Logical gates")
print("-------------------")

# Set up the basic matrices


print("Vector representations of our bits:")
print("-------------------------------------")

bits = {"b0":np.array([1,0]), "b1":np.array([0,1])}

for b in bits:
  print(b, "\n", bits[b]) 
print ("\n")

print("Matrix representations of our gates:")
print("-------------------------------------")
gates ={"id":np.array([[1, 0], [0, 1]]),"not":np.array([[0, 1], [1, 0]])}

for g in gates:
  print(g, "\n", gates[g].round()) 
print ("\n")

# Now, let's apply the defined gates on our qubits.
# Matrix manipulations

print("Gate manipulations of our bits:")
print("-------------------------------")

for g in gates:
    print("Gate:",g) 
    for b in bits:
        print(b,bits[b],"->", np.dot(gates[g],bits[b])) 
    print("\n")

print("Vector representations of our two bits:")
print("---------------------------------------")

twobits = {"b00":np.array([1,0,0,0]), "b01":np.array([0,1,0,0]),"b10":np.array([0,0,1,0]),"b11":np.array([0,0,0,1]),}

for b in twobits:
  print(b, "\n", twobits[b]) 
print ("\n")

print("Matrix representations of our gates:")
print("------------------------------------")
twogates ={"and":np.array([[1, 1, 1, 0], [0, 0, 0, 1]]), "or":np.array([[1, 0, 0, 0], [0, 1, 1, 1]])}

for g in twogates:
  print(g, "\n", twogates[g].round()) 
print ("\n")

# Matrix manipulations

print("Gate manipulations of our bits:")
print("-------------------------------")

for g in twogates:
    print("Gate:",g) 
    for b in twobits:
        print(b,twobits[b],"->", np.dot(twogates[g],twobits[b])) 
    print("\n")

