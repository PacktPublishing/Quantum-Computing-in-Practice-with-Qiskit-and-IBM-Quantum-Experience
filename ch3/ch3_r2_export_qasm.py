#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For this simple recipe we will only need the QuantumCircuit method
from qiskit.circuit.random.utils import random_circuit

print("Ch 3: Moving between worlds 2")
print("-----------------------------")

# First we create and print a random quantum circuit
print("Random quantum circuit")
print("----------------------\n")
circ=random_circuit(5,5,measure=True)
print(circ)


# Next, we export the circuit as QASM code. If you include a filename you can also save the QASM code as a text file on your local machine
print("\nOpenQASM code")
print("-------------\n")

circ.qasm(formatted=True, filename="Circuit.qasm")


