#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:07:00 2019

@author: hnorlen
"""

from qiskit import QuantumCircuit, Aer, execute
from qiskit.tools.visualization import plot_histogram
from IPython.core.display import display

print("Ch 4: Quantum double coin toss")
print("------------------------------")

qc = QuantumCircuit(2, 2)

qc.h([0,1])
qc.measure([0,1],[0,1])

display(qc.draw('mpl'))

backend = Aer.get_backend('qasm_simulator')
counts = execute(qc, backend, shots=1).result().get_counts(qc)

display(plot_histogram(counts))


