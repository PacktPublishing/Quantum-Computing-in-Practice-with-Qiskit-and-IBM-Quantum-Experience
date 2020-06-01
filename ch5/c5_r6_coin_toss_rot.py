#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:07:00 2019

@author: hnorlen
"""

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, execute
from math import pi
from math import sqrt

q = QuantumRegister(1)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)

qc.h(q[0])
qc.ry(pi/8,q) 
qc.measure(q, c)

print(qc)

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1)
result = job.result()
counts = result.get_counts(qc)
print(counts)

from qiskit.tools.visualization import plot_histogram
display(plot_histogram(counts))
              
from qiskit.tools.visualization import plot_bloch_vector
#Display the Bloch vector for|0>.
display(plot_bloch_vector([0,0,1], title='Qubit in ground state |0>') )

from qiskit.tools.visualization import plot_bloch_vector
#Display the Bloch vector for|0>.
plot_bloch_vector([1,0,0], title='Qubit in super position') 

from qiskit.tools.visualization import plot_bloch_vector
#Display the Bloch vector for|0>.
plot_bloch_vector([0.924,0,-0.383], title='Qubit pi/8 radians closer to |1>') 