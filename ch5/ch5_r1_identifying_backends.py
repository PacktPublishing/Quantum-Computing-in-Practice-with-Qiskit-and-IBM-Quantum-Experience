#!/usr/bin/env python
# coding: utf-8

from qiskit import IBMQ, QuantumCircuit, execute
from qiskit.tools.monitor import job_monitor

print("Ch 5: Identifying backends")
print("--------------------------")

print("Getting provider...")
if not IBMQ.active_account():
    IBMQ.load_account()
provider = IBMQ.get_provider()

print("\nAvailable backends:")
print(provider.backends(operational=True, simulator=False))

backend = provider.get_backend('ibmqx2')
print("\nSelected backend:", backend.name())

# Create a quantum circuit to test
qc = QuantumCircuit(2,2)

qc.h(0)
qc.cx(0,1)
qc.measure([0,1],[0,1])

print("\nQuantum circuit:")
print(qc)

job = execute(qc, backend, shots=1000)
job_monitor(job)

result = job.result()
counts = result.get_counts(qc)

print("\nResults:", counts)

print("\nAvailable simulator backends:")
print(provider.backends(operational=True, simulator=True))

backend = provider.get_backend('ibmq_qasm_simulator')
job = execute(qc, backend, shots=1000)
job_monitor(job)

result = job.result()
counts = result.get_counts(qc)

print("\nSimulator results:", counts) 





