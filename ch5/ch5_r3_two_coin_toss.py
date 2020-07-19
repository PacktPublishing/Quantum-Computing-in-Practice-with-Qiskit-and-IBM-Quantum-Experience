#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:07:00 2019

@author: hnorlen
"""

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, execute

from IPython.core.display import display

q = QuantumRegister(2)
c = ClassicalRegister(2)
qc = QuantumCircuit(q, c)

qc.h(q)
qc.measure(q, c)

display(qc.draw('mpl'))

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1)
result = job.result()
counts = result.get_counts(qc)
print(counts)

from qiskit.tools.visualization import plot_histogram
display(plot_histogram(counts))


