#!/usr/bin/env python
# coding: utf-8

from qiskit import IBMQ
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, execute
from qiskit.tools.monitor import job_monitor

IBMQ.load_account()
provider = IBMQ.get_provider()

print("Available backends:")
print(provider.backends(operational=True, simulator=False))

backend = provider.get_backend('ibmqx2')
print("Selected backend:", backend.name())

q = QuantumRegister(2)
c = ClassicalRegister(2)
qc = QuantumCircuit(q, c)

qc.h(q[0])
qc.cx(q[0],q[1])
qc.measure(q, c)

print("Quantum circuit:")
print(qc)

job = execute(qc, backend, shots=1000)
job_monitor(job)

result = job.result()
counts = result.get_counts(qc)

print("Results:", counts)

print("Available simulator backends:")
print(provider.backends(operational=True, simulator=True))

backend = provider.get_backend('ibmq_qasm_simulator')
job = execute(qc, backend, shots=1000)
job_monitor(job)

result = job.result()
counts = result.get_counts(qc)

print("Simulator results:", counts) 





