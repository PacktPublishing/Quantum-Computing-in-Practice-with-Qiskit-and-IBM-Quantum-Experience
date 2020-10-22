#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:07:00 2019

@author: hnorlen
"""

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, execute
from qiskit.tools.visualization import plot_histogram

from IPython.core.display import display

print("Ch 4: Quantum coin toss")
print("-----------------------")

q = QuantumRegister(1)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)

qc.h(q[0])
qc.measure(q, c)

display(qc.draw('mpl'))
print(qc)
display(qc.draw('text'))


backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1)
result = job.result()
counts = result.get_counts(qc)

print(counts)
display(plot_histogram(counts))
        
