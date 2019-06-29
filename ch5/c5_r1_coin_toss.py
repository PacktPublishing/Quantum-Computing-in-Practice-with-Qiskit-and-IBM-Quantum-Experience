#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:07:00 2019

@author: hnorlen
"""

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, execute

q = QuantumRegister(1)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)

qc.h(q[0])
qc.measure(q, c)

print(qc)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1)
result = job.result()
counts = result.get_counts(qc)
print(counts)

from qiskit.tools.visualization import plot_histogram
plot_histogram(counts)
              
from qiskit.tools.visualization import plot_bloch_vector
#Create an empty dictionary for the two possible states.
counts_dict = {'0': 0, '1': 0} 
#Merge in the actual result.
counts_dict.update(counts) 
#Display the Bloch vector with the result as 0 or 1 on the Z-axis.
plot_bloch_vector([0,0,(counts_dict['0']-counts_dict['1'])]) 