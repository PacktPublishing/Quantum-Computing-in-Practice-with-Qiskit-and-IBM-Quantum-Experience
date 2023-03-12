#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Nov 2020, verified March 2023

@author: hassi
"""

from qiskit import QuantumCircuit, Aer, execute
from qiskit.tools.visualization import plot_histogram
from IPython.core.display import display

print("Ch 4: Cheating quantum coin toss")
print("--------------------------------")

qc = QuantumCircuit(2, 2)

qc.h(0)
qc.cx(0,1)
qc.measure([0,1],[0,1])

display(qc.draw('mpl'))

backend = Aer.get_backend('qasm_simulator')
counts = execute(qc, backend, shots=1000).result().get_counts(qc)

display(plot_histogram(counts))


