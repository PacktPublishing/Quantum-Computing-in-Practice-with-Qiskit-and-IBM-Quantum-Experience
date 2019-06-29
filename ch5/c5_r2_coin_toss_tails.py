#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:07:00 2019

@author: hnorlen
"""

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, execute
import matplotlib
matplotlib.use('Cairo')

q = QuantumRegister(1)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)

qc.x(q[0])
qc.h(q[0])
qc.measure(q, c)

print(qc)

backend = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend, shots=1)
sim_result = job_sim.result()

counts = sim_result.get_counts(qc)
              
from qiskit.visualization import plot_histogram
plot_histogram(counts).show()