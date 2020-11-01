#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020

@author: hassi
"""

# For this simple recipe we will only need the QuantumCircuit method
from qiskit import QuantumCircuit

print("Ch 3: Moving between worlds 1")
print("-----------------------------")

# First we import the QASM string from IBM Qx
qasm_string=input("Paste in a QASM string from IBM Qx (or enter the full path and file name of a .qasm file to import):\n")

if qasm_string[-5:] == ".qasm":
    # Create a quantum circuit from the file
    circ=QuantumCircuit.from_qasm_file(qasm_string)
else:
    # Create a quantum circuit from the string
    circ=QuantumCircuit.from_qasm_str(qasm_string)

# Print the circuitCoin.qasm
print("Imported quantum circuit")    
print("------------------------")    
print(circ)
