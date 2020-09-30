#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:07:00 2019

@author: hnorlen
"""

from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

from IPython.core.display import display

print("Ch 4: Upside down quantum coin toss")
print("-----------------------------------")


qc = QuantumCircuit(1, 1)
initial_vector = [0.+0.j, 1.+0.j]
qc.initialize(initial_vector,0)

#qc.x(0)
qc.h(0)
qc.measure(0, 0)

print(qc)
#display(qc.draw())

backend = Aer.get_backend('qasm_simulator')

counts = execute(qc, backend, shots=1).result().get_counts(qc)
              
display(plot_histogram(counts))