#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:07:00 2019

@author: hnorlen
"""

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, execute

from qiskit import IBMQ
from qiskit.tools.monitor import job_monitor

from IPython.core.display import display

IBMQ.load_account()
provider = IBMQ.get_provider()

q = QuantumRegister(2)
c = ClassicalRegister(2)
qc = QuantumCircuit(q, c)

qc.h(q[0])
qc.cx(q[0],q[1])
qc.measure(q, c)

display(qc.draw('mpl'))

from qiskit.providers.ibmq import least_busy
backend = least_busy(provider.backends(n_qubits=5, operational=True, simulator=False))
print(backend.name())


job = execute(qc, backend, shots=1000)
job_monitor(job)

result = job.result()
counts = result.get_counts(qc)
print(counts)

print(result)