#!/usr/bin/env python
# coding: utf-8

print("Ch 8: Boiling down your circuits with the unitary simulator")
print("-----------------------------------------------------------")

# Import the required Qiskit classes
from qiskit import(
  QuantumCircuit,
  execute,
  Aer)

# Import some math that we might need
from math import pi, sqrt, pow

import numpy as np
np.set_printoptions(precision=3)

print("Vector representations of our qubits:")
print("-------------------------------------")

qubits = {"q0":np.array([1,0]), "q1":np.array([0,1]), "qh":1/sqrt(2)*np.array([1,1]), "2q00":np.array([1,0,0,0])}
print(qubits)

# Choose unitary simulator.
backend = Aer.get_backend('unitary_simulator') 

# Create the required registers and the quantum circuit
qc = QuantumCircuit(1,1)
print(qc)
qc.depth()

# Get the unitary
unit=execute(qc, backend).result().get_unitary(qc)
print(unit)

# Add a Hadamard gate
qc.h(0)
display(qc.draw())

# Get the unitary
unit=execute(qc, backend).result().get_unitary(qc)
print(unit)

# Add a Pauli Z gate
qc.z(0)
display(qc.draw())
print(qc.depth())

# Get the unitary
unit=execute(qc, backend).result().get_unitary(qc)
print(unit)

# Add a measure gate
qc.measure(0,0)
display(qc.draw())

# Run the circuit on the QASM simulator
backend_count = Aer.get_backend('qasm_simulator') 
counts=execute(qc, backend_count,shots=backend.configuration().max_shots).result().get_counts(qc)
print("Executed:",counts)
a_and_b=np.dot(unit,qubits['q1'])
print("Calculated: '0':",pow(abs(a_and_b[0]),2),"'1':",pow(abs(a_and_b[1]),2))


## Two qubit states

# Create the required registers and the quantum circuit
qc = QuantumCircuit(2,2)
display(qc.draw())

# Get the unitary
unit=execute(qc, backend).result().get_unitary(qc)
print(unit)

qc.x(0)
display(qc.draw())

# Get the unitary
unit=execute(qc, backend).result().get_unitary(qc)
print(unit)

qc.swap(0,1)
display(qc.draw())

# Get the unitary
unit=execute(qc, backend).result().get_unitary(qc)
print(unit)

qc.measure([0,1],[0,1])
display(qc.draw())

backend_count = Aer.get_backend('qasm_simulator') 
counts=execute(qc, backend_count,shots=backend.configuration().max_shots).result().get_counts(qc)
print("Executed:",counts)
a_thru_d=np.dot(unit,qubits['2q00'])
print(a_thru_d)
print("Calculated: '00':",pow(abs(a_thru_d[0]),2),"'01':",pow(abs(a_thru_d[1]),2),"'10':",pow(abs(a_thru_d[2]),2),"'11':",pow(abs(a_thru_d[3]),2))


## Entangled states

# Create the required registers and the quantum circuit
qc = QuantumCircuit(2,2)
display(qc.draw())


# Get the unitary
unit=execute(qc, backend).result().get_unitary(qc)
print(unit)
print(abs(unit))

qc.h(0)
display(qc.draw())

# Get the unitary
unit=execute(qc, backend).result().get_unitary(qc)
print(unit)

qc.cx(0,1)
display(qc.draw())

# Get the unitary
unit=execute(qc, backend).result().get_unitary(qc)
print(unit)

qc.x(0)
display(qc.draw())

# Get the unitary
unit=execute(qc, backend).result().get_unitary(qc)
print(unit)

qc.measure(0,0)
qc.measure(1,1)
display(qc.draw())

backend_count = Aer.get_backend('qasm_simulator') 
counts=execute(qc, backend_count,shots=1000).result().get_counts(qc)
print("Executed:",counts)
a_thru_d=np.dot(unit,qubits['2q00'])
print(a_thru_d)
print("Calculated: '00':",pow(abs(a_thru_d[0]),2),"'01':",pow(abs(a_thru_d[1]),2),"'10':",pow(abs(a_thru_d[2]),2),"'11':",pow(abs(a_thru_d[3]),2))




