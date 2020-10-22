#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 03 2020

@author: hassi
"""

from qiskit import QuantumCircuit, Aer, execute
from IPython.core.display import display
from qiskit.tools.visualization import plot_histogram

print("Ch 9: Grover with ancilla qubits")
print("--------------------------------")

# Create 3 qubit circuit with two classical bits
qc=QuantumCircuit(3,2)


qc.h([0,1])
qc.x(2)

# Code for the oracle
qc.barrier([0,1,2])
qc.x(0)
qc.barrier([0,1,2])

# Phase kickback using the ancilla qubit
qc.h(2)
qc.ccx(0,1,2)
qc.h(2)

# End code for the oracle
qc.barrier([0,1,2])
qc.x(0)
qc.barrier([0,1,2])

# Amplifier
qc.h([0,1])
qc.x([0,1])
qc.h(1)
qc.cx(0,1)
qc.h(1)
qc.barrier([0,1,2])
qc.x([0,1])
qc.h([0,1])

# Measure two qubits
qc.measure([0,1],[0,1])

# Display circuit and execute on simulator
display(qc.draw('mpl'))

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1)
result = job.result()
counts = result.get_counts(qc)

display(plot_histogram(counts))
